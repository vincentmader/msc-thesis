from numba import jit
import utils

@jit(nopython=True)
def K_gain(k, i, j):
    return 1/2 * utils.kronecker_delta(k, i+j)

@jit(nopython=True)
def K_loss(k, i, j):
    return utils.kronecker_delta(k, i)

