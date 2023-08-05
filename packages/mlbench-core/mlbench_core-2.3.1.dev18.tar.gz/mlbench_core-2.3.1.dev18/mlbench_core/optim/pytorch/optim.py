import numpy as np
import torch
import torch.distributed as dist
from mlbench_core.utils.pytorch.distributed import AllReduceAggregation
from mlbench_core.utils.pytorch.distributed import DecentralizedAggregation
from torch.nn.utils import clip_grad_norm_
from torch.optim import SGD
from torch.optim.optimizer import Optimizer, required
from apex import amp

import math


class SparsifiedSGD(Optimizer):
    r"""Implements sparsified version of stochastic gradient descent.

    Args:
        params (iterable): iterable of parameters to optimize or dicts defining
            parameter groups
        lr (float): learning rate
        weight_decay (float, optional): weight decay (L2 penalty) (default: 0)
        sparse_grad_size (int): Size of the sparsified gradients vector (
        default: 10).

    """

    def __init__(self, params, lr=required, weight_decay=0, sparse_grad_size=10):

        if lr is not required and lr < 0.0:
            raise ValueError("Invalid learning rate: {}".format(lr))
        if weight_decay < 0.0:
            raise ValueError("Invalid weight_decay value: {}".format(weight_decay))

        defaults = dict(lr=lr, weight_decay=weight_decay)

        super(SparsifiedSGD, self).__init__(params, defaults)

        self.__create_gradients_memory()
        self.__create_weighted_average_params()

        self.num_coordinates = sparse_grad_size

    def __create_weighted_average_params(self):
        r""" Create a memory to keep the weighted average of parameters in
        each iteration """
        for group in self.param_groups:
            for p in group["params"]:
                param_state = self.state[p]
                param_state["estimated_w"] = torch.zeros_like(p.data)
                p.data.normal_(0, 0.01)
                param_state["estimated_w"].copy_(p.data)

    def __create_gradients_memory(self):
        r""" Create a memory to keep gradients that are not used in each
        iteration """
        for group in self.param_groups:
            for p in group["params"]:
                param_state = self.state[p]
                param_state["memory"] = torch.zeros_like(p.data)

    def step(self, closure=None):
        """Performs a single optimization step.

        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
        """
        loss = None
        if closure is not None:
            loss = closure()

        for group in self.param_groups:

            weight_decay = group["weight_decay"]

            for p in group["params"]:

                if p.grad is None:
                    continue
                d_p = p.grad.data

                if weight_decay != 0:
                    d_p.add_(weight_decay, p.data)
                p.data.add_(-d_p)

        return loss

    def sparsify_gradients(self, param, lr):
        """ Calls one of the sparsification functions (random or blockwise)

        Args:
            random_sparse (bool): Indicates the way we want to make the
            gradients sparse
                (random or blockwise) (default: False)
            param (:obj: `torch.nn.Parameter`): Model parameter
        """
        if self.random_sparse:
            return self._random_sparsify(param, lr)
        else:
            return self._block_sparsify(param, lr)

    def _random_sparsify(self, param, lr):
        """ Sparsify the gradients vector by selecting 'k' of them randomly.

        Args:
            param (:obj: `torch.nn.Parameter`): Model parameter
            lr (float): Learning rate

        """

        self.state[param]["memory"] += param.grad.data * lr

        indices = np.random.choice(
            param.data.size()[1], self.num_coordinates, replace=False
        )
        sparse_tensor = torch.zeros(2, self.num_coordinates)

        for i, random_index in enumerate(indices):
            sparse_tensor[1, i] = self.state[param]["memory"][0, random_index]
            self.state[param]["memory"][0, random_index] = 0
        sparse_tensor[0, :] = torch.tensor(indices)

        return sparse_tensor

    def _block_sparsify(self, param, lr):
        """ Sparsify the gradients vector by selecting a block of them.

        Args:
            param (:obj: `torch.nn.Parameter`): Model parameter
            lr (float): Learning rate
        """

        self.state[param]["memory"] += param.grad.data * lr

        num_block = int(param.data.size()[1] / self.num_coordinates)

        current_block = np.random.randint(0, num_block)
        begin_index = current_block * self.num_coordinates

        end_index = begin_index + self.num_coordinates - 1
        output_size = 1 + end_index - begin_index + 1

        sparse_tensor = torch.zeros(1, output_size)
        sparse_tensor[0, 0] = begin_index
        sparse_tensor[0, 1:] = self.state[param]["memory"][
            0, begin_index : end_index + 1
        ]
        self.state[param]["memory"][0, begin_index : end_index + 1] = 0

        return sparse_tensor

    def update_estimated_weights(self, iteration, sparse_vector_size):
        """ Updates the estimated parameters

        Args:
            iteration (int): Current global iteration
            sparse_vector_size (int): Size of the sparse gradients vector
        """
        t = iteration
        for group in self.param_groups:
            for param in group["params"]:
                tau = param.data.size()[1] / sparse_vector_size
                rho = (
                    6
                    * ((t + tau) ** 2)
                    / ((1 + t) * (6 * (tau ** 2) + t + 6 * tau * t + 2 * (t ** 2)))
                )
                self.state[param]["estimated_w"] = (
                    self.state[param]["estimated_w"] * (1 - rho) + param.data * rho
                )

    def get_estimated_weights(self):
        """ Returns the weighted average parameter tensor """
        estimated_params = []
        for group in self.param_groups:
            for param in group["params"]:
                estimated_params.append(self.state[param]["estimated_w"])
        return estimated_params


class CentralizedSparsifiedSGD(SparsifiedSGD):
    r"""Implements centralized sparsified version of stochastic gradient
    descent.

    Args:
        params (iterable): iterable of parameters to optimize or dicts defining
            parameter groups
        lr (float): Learning rate
        weight_decay (float, optional): weight decay (L2 penalty) (default: 0)
        sparse_grad_size (int): Size of the sparsified gradients vector (
        default: 10)
        random_sparse (bool): Whether select random sparsification (default:
        `False`)
        average_models (bool): Whether to average models together (default:
        `True`)

    """

    def __init__(
        self,
        params,
        lr=required,
        weight_decay=0,
        sparse_grad_size=10,
        random_sparse=False,
        average_models=True,
    ):
        self.average_models = average_models
        self.world_size = dist.get_world_size()
        self.random_sparse = random_sparse
        super(CentralizedSparsifiedSGD, self).__init__(
            params, lr, weight_decay, sparse_grad_size
        )

    def step(self, closure=None):
        """ Aggregates the gradients and performs a single optimization step.

            Arguments:
                closure (callable, optional): A closure that reevaluates the
                model and returns the loss.
        """

        loss = None

        if closure is not None:
            loss = closure()

        for group in self.param_groups:

            weight_decay = group["weight_decay"]
            lr = group["lr"]

            for p in group["params"]:
                # Sparsify the gradients
                sparse_tensor = self.sparsify_gradients(p, lr)
                # Aggregate the gradients
                gathered_list = [
                    torch.zeros_like(sparse_tensor) for _ in range(self.world_size)
                ]
                dist.all_gather(gathered_list, sparse_tensor)
                p.grad.data = torch.zeros_like(p.grad.data)

                if self.random_sparse:
                    for grad_tensor in gathered_list:
                        for index in range(grad_tensor.size()[1]):
                            p.grad.data[0, int(grad_tensor[0, index])] += grad_tensor[
                                1, index
                            ]
                else:
                    for grad_tensor in gathered_list:
                        tensor_size = grad_tensor.size()[1]
                        begin = int(grad_tensor[0, 0])
                        p.grad.data[
                            0, begin : (begin + tensor_size - 1)
                        ] += grad_tensor[0, 1:]

                if self.average_models:
                    p.grad.data /= self.world_size

                if p.grad is None:
                    continue
                d_p = p.grad.data

                if weight_decay != 0:
                    d_p.add_(weight_decay, p.data)
                p.data.add_(-d_p)

        return loss


class DecentralizedSGD(SGD):
    r"""Implements decentralized stochastic gradient descent (optionally
    with momentum).

    Args:
        rank (int): rank of current process in the network
        neighbors (list): list of ranks of the neighbors of current process
        model (:obj:`nn.Module`): model which contains parameters for SGD
        lr (float): learning rate
        momentum (float, optional): momentum factor (default: 0)
        weight_decay (float, optional): weight decay (L2 penalty) (default: 0)
        dampening (float, optional): dampening for momentum (default: 0)
        nesterov (bool, optional): enables Nesterov momentum (default: False)
        average_models (bool): Whether to average models together. (default:
        `True`)

    """

    def __init__(
        self,
        rank,
        neighbors,
        model,
        lr=required,
        momentum=0,
        dampening=0,
        weight_decay=0,
        nesterov=False,
        average_models=True,
    ):
        super(DecentralizedSGD, self).__init__(
            model.parameters(), lr, momentum, dampening, weight_decay, nesterov
        )

        if average_models:
            self.agg_mode = "avg"
        else:
            raise NotImplementedError("Only average model is supported right now.")

        self.model = model
        self.agg = DecentralizedAggregation(rank, neighbors).agg_model

    def step(self, closure=None):
        """ Aggregates the gradients and performs a single optimization step.

        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
        """
        loss = super(DecentralizedSGD, self).step(closure=closure)
        # Averaging the model after updating the gradient separately.
        self.agg(self.model, self.agg_mode)
        return loss


class CentralizedSGD(SGD):
    r"""Implements centralized stochastic gradient descent (optionally with
    momentum).

    Args:
        world_size (int): Size of the network
        model (:obj:`nn.Module`): Model which contains parameters for SGD
        lr (float): learning rate
        momentum (float, optional): momentum factor (default: 0)
        weight_decay (float, optional): weight decay (L2 penalty) (default: 0)
        dampening (float, optional): dampening for momentum (default: 0)
        nesterov (bool, optional): enables Nesterov momentum (default: False)
        average_models (bool): Whether to average models together. (default:
        `True`)

    """

    def __init__(
        self,
        world_size,
        model,
        lr=required,
        momentum=0,
        dampening=0,
        weight_decay=0,
        nesterov=False,
        average_models=True,
    ):
        super(CentralizedSGD, self).__init__(
            model.parameters(), lr, momentum, dampening, weight_decay, nesterov
        )
        if average_models:
            self.agg_mode = "avg"
        else:
            raise NotImplementedError("Only average model is supported right now.")

        self.model = model
        self.agg = AllReduceAggregation(world_size=world_size).agg_grad

    def step(self, closure=None):
        """ Aggregates the gradients and performs a single optimization step.

        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
        """
        self.agg(self.model, self.agg_mode)
        loss = super(CentralizedSGD, self).step(closure=closure)
        return loss


class SignSGD(SGD):
    r"""Implements sign stochastic gradient descent (optionally with momentum).

    Args:
        params (iterable): iterable of parameters to optimize or dicts defining
            parameter groups
        lr (float): learning rate
        momentum (float, optional): momentum factor (default: 0)
        weight_decay (float, optional): weight decay (L2 penalty) (default: 0)
        dampening (float, optional): dampening for momentum (default: 0)
        nesterov (bool, optional): enables Nesterov momentum (default: False)
        average_models (bool): Whether to average models together. (default:
        `True`)

    """

    def step(self, closure=None):
        """ Aggregates the gradients and performs a single optimization step.

        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
        """
        loss = None
        if closure is not None:
            loss = closure()

        for group in self.param_groups:
            weight_decay = group["weight_decay"]
            momentum = group["momentum"]
            dampening = group["dampening"]
            nesterov = group["nesterov"]

            for p in group["params"]:
                if p.grad is None:
                    continue
                d_p = p.grad.data
                if weight_decay != 0:
                    d_p.add_(weight_decay, p.data)
                if momentum != 0:
                    param_state = self.state[p]
                    if "momentum_buffer" not in param_state:
                        buf = param_state["momentum_buffer"] = torch.zeros_like(p.data)
                        buf.mul_(momentum).add_(d_p)
                    else:
                        buf = param_state["momentum_buffer"]
                        buf.mul_(momentum).add_(1 - dampening, d_p)
                    if nesterov:
                        d_p = d_p.add(momentum, buf)
                    else:
                        d_p = buf

                # Update with the sign
                p.data.add_(-group["lr"], torch.sign(d_p))

        return loss


class FP32Optimizer:
    """
    Standard optimizer, computes backward and applies weight update.
    """

    def __init__(self, model, optimizer, grad_clip=None):
        """
        Constructor for the Fp32Optimizer

        :param grad_clip: coefficient for gradient clipping, max L2 norm of the
            gradients
        """
        self.params = model.parameters()
        self.grad_clip = grad_clip
        self.optimizer = optimizer

    def step(self):
        """
        Performs one step of the optimizer.

        :param loss: value of loss function
        :param optimizer: optimizer
        :param update: if True executes weight update
        """
        if self.grad_clip != float("inf"):
            clip_grad_norm_(self.params, self.grad_clip)
        self.optimizer.step()

    def backward_loss(self, loss):
        loss.backward()

    def zero_grad(self):
        self.optimizer.zero_grad()


class FP16Optimizer:
    """
    Mixed precision optimizer with dynamic loss scaling and backoff.
    https://docs.nvidia.com/deeplearning/sdk/mixed-precision-training/index
    .html#scalefactor
    """

    @staticmethod
    def set_grads(params, params_with_grad):
        """
        Copies gradients from param_with_grad to params

        :param params: dst parameters
        :param params_with_grad: src parameters
        """
        for param, param_w_grad in zip(params, params_with_grad):
            if param.grad is None:
                param.grad = torch.nn.Parameter(torch.empty_like(param))
            param.grad.data.copy_(param_w_grad.grad.data)

    @staticmethod
    def set_weights(params, new_params):
        """
        Copies parameters from new_params to params

        :param params: dst parameters
        :param new_params: src parameters
        """
        for param, new_param in zip(params, new_params):
            param.data.copy_(new_param.data)

    def __init__(
        self,
        model,
        optimizer,
        grad_clip=float("inf"),
        loss_scale=8192,
        dls_downscale=2,
        dls_upscale=2,
        dls_upscale_interval=128,
    ):
        """
        Constructor for the Fp16Optimizer.

        :param model: model
        :param grad_clip: coefficient for gradient clipping, max L2 norm of the
            gradients
        :param loss_scale: initial loss scale
        :param dls_downscale: loss downscale factor, loss scale is divided by
            this factor when NaN/INF occurs in the gradients
        :param dls_upscale: loss upscale factor, loss scale is multiplied by
            this factor if previous dls_upscale_interval batches finished
            successfully
        :param dls_upscale_interval: interval for loss scale upscaling
        """
        self.initialize_model(model)

        self.optimizer = optimizer
        self.since_last_invalid = 0
        self.loss_scale = loss_scale
        self.dls_downscale = dls_downscale
        self.dls_upscale = dls_upscale
        self.dls_upscale_interval = dls_upscale_interval
        self.grad_clip = grad_clip

    def set_optimizer(self, optimizer):
        self.optimizer = optimizer

    def initialize_model(self, model):
        """
        Initializes internal state and build fp32 master copy of weights.

        :param model: fp16 model
        """
        model.half()
        self.model = model
        self.model.zero_grad()
        self.fp32_params = [
            param.to(torch.float32).detach() for param in model.parameters()
        ]

        for param in self.fp32_params:
            param.requires_grad = True

    def backward_loss(self, loss):
        loss *= self.loss_scale
        loss.backward()

    def step(self):
        """
        Performs one step of the optimizer.
        Applies loss scaling, computes gradients in fp16, converts gradients to
        fp32, inverts scaling and applies optional gradient norm clipping.
        If gradients are finite, it applies update to fp32 master weights and
        copies updated parameters to fp16 model for the next iteration. If
        gradients are not finite, it skips the batch and adjusts scaling factor
        for the next iteration.

        :param loss: value of loss function
        :param optimizer: optimizer
        :param update: if True executes weight update
        """
        self.set_grads(self.fp32_params, self.model.parameters())
        if self.loss_scale != 1.0:
            for param in self.fp32_params:
                param.grad.data /= self.loss_scale

        norm = clip_grad_norm_(self.fp32_params, self.grad_clip)

        if math.isfinite(norm):
            self.optimizer.step()
            self.set_weights(self.model.parameters(), self.fp32_params)
            self.since_last_invalid += 1
        else:
            self.loss_scale /= self.dls_downscale
            self.since_last_invalid = 0

        if self.since_last_invalid >= self.dls_upscale_interval:
            self.loss_scale *= self.dls_upscale
            self.loss_scale = min(self.loss_scale, 8192.0)
            self.since_last_invalid = 0

    def zero_grad(self):
        self.optimizer.zero_grad()


class AMPOptimizer:
    """
    Optimizer compatible with AMP.
    Uses AMP to apply loss scaling, computes backward and applies weight
    update.
    """

    def __init__(
        self,
        model,
        optimizer,
        grad_clip=None,
        loss_scale=8192,
        dls_upscale_interval=128,
    ):
        """
        Constructor for the AMPOptimizer

        :param model: model
        :param grad_clip: coefficient for gradient clipping, max L2 norm of the
            gradients
        """
        self.grad_clip = grad_clip
        self.optimizer = optimizer
        loss_scaler = amp._amp_state.loss_scalers[0]
        loss_scaler._loss_scale = loss_scale
        loss_scaler._scale_seq_len = dls_upscale_interval

    def backward_loss(self, loss):
        with amp.scale_loss(loss, self.optimizer) as scaled_loss:
            scaled_loss.backward()

    def step(self):
        """
        Performs one step of the optimizer.

        :param loss: value of loss function
        :param optimizer: optimizer
        :param update: if True executes weight update
        """
        if self.grad_clip != float("inf"):
            clip_grad_norm_(amp.master_params(self.optimizer), self.grad_clip)
        self.optimizer.step()

    def zero_grad(self):
        self.optimizer.zero_grad()
