import numpy as np
from numba import jit


def gaussian(x, mu, sigma):
    y = np.exp(-((x-mu)/sigma)**2) / ((2*np.pi)**.5 * sigma)
    return y


def dirac_delta(x, i_x0):
    y = np.zeros(len(x))
    y[i_x0] = 1
    return y


@jit(nopython=True)
def kronecker_delta(i, j):
    return 1 if i == j else 0
