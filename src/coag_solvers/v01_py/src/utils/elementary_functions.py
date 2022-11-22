import numpy as np
from numba import njit


@njit()
def gaussian(x, mu, sigma):
    y = np.exp(-((x-mu)/sigma)**2) / ((2*np.pi)**.5 * sigma)
    return y


@njit()
def dirac_delta(x, i_x0):
    y = np.zeros(len(x))
    y[i_x0] = 1
    return y


@njit()
def kronecker_delta(i, j):
    return 1 if i == j else 0


@njit()
def heaviside_theta(x):
    if x < 0:
        return 0
    elif x == 0:
        return 1/2
    else:
        return 1
