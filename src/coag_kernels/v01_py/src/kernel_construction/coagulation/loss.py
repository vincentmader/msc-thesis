import numpy as np

from config import Config
from kernel_construction.collision import collision_and_merge_rate as R


def construct_loss_term(cfg: Config):
    # Initialize kernel as 3D matrix of zeros.
    K = np.zeros(shape=[cfg.mass_grid_resolution]*3)

    indices = np.arange(0, K.shape[0], 1)

    # Loop over all possible particle-particle pairs in the discrete mass grid.
    for i in indices:
        for j in indices:
            R_kij = R(i, j, cfg)
            K[i, i, j] -= R_kij

    return K
