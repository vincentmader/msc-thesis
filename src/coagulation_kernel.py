from numba import jit
import utils

@jit(nopython=True, cache=True)
def K(k, i, j):
    K_g = K_gain(k, i, j) * utils.kronecker_delta(k, i+j)
    K_l = K_loss(k, i, j) * utils.kronecker_delta(k, i)
    return K_g - K_l


@jit(nopython=True, cache=True)
def K_gain(k, i, j):
    return 1/2


@jit(nopython=True, cache=True)
def K_loss(k, i, j):
    return 1

