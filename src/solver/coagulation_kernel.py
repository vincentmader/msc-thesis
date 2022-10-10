import numpy as np
from numba import jit

from config import GRID_RESOLUTION
import utils


@jit(nopython=True, cache=True)
def create_coagulation_kernel():
    K = np.zeros((GRID_RESOLUTION, GRID_RESOLUTION, GRID_RESOLUTION))
    for k in range(GRID_RESOLUTION):
        for i in range(GRID_RESOLUTION):
            for j in range(GRID_RESOLUTION):
                K[k][i][j] = K_kij(k, i, j)
    return K


@jit(nopython=True, cache=True)
def K_kij(k, i, j):
    K_g = K_kij_gain(k, i, j) * utils.kronecker_delta(k, i+j)
    K_l = K_kij_loss(k, i, j) * utils.kronecker_delta(k, i)
    return K_g - K_l


@jit(nopython=True, cache=True)
def K_kij_gain(k, i, j):
    return 1/2


@jit(nopython=True, cache=True)
def K_kij_loss(k, i, j):
    return 1
