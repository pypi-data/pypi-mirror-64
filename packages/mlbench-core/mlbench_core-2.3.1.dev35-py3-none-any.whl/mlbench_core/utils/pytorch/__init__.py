import torch.distributed as dist
from .helpers import config_logging
from .helpers import config_pytorch
from .helpers import config_path
from .helpers import Timeit
from .topology import FCGraph

from contextlib import contextmanager
import os

__all__ = ["initialize_backends", "Timeit", "FCGraph"]


@contextmanager
def initialize_backends(
    comm_backend="mpi",
    logging_level="INFO",
    logging_file="/mlbench.log",
    use_cuda=False,
    seed=None,
    cudnn_deterministic=False,
    ckpt_run_dir="/checkpoints",
    delete_existing_ckpts=False,
):
    """Initializes the backends.

    Sets up logging, sets up pytorch and configures paths
    correctly.

    Args:
        config (:obj:`types.SimpleNamespace`): a global object containing all of the config.

    Returns:
        (:obj:`types.SimpleNamespace`): a global object containing all of the config.
    """

    if not (hasattr(dist, "_initialized") and dist._initialized):

        if (comm_backend == "mpi"):
            dist.init_process_group(comm_backend)
        else:

            required_vars = ["KUBERNETES_SERVICE_HOST", 
                            "KUBERNETES_SERVICE_PORT", 
                            "OMPI_COMM_WORLD_SIZE",
                            "OMPI_COMM_WORLD_RANK"]

            for env in required_vars:
                assert(os.getenv(env) is not None,
                    "Missing required environment variable: " + env)
            
            os.environ["MASTER_ADDR"] = os.getenv("KUBERNETES_SERVICE_HOST")
            os.environ["MASTER_PORT"] = os.getenv("KUBERNETES_SERVICE_PORT")
            dist.init_process_group(
                backend=comm_backend,
                world_size=os.getenv("OMPI_COMM_WORLD_SIZE"),
                rank=os.getenv("OMPI_COMM_WORLD_RANK")
            )

    config_logging(logging_level, logging_file)

    rank, world_size, graph = config_pytorch(use_cuda, seed, cudnn_deterministic)

    config_path(ckpt_run_dir, delete_existing_ckpts)

    yield rank, world_size, graph

    dist.destroy_process_group()
