import numpy as np
from numba import jit

from config import GRID_RESOLUTION as GRID_RES
from utils.elementary_functions import kronecker_delta


@jit(nopython=True)
def dn_k(K_gain, K_loss, n, k):
    out = 0

    for i in range(GRID_RES):
        for j in range(GRID_RES):
            out += 1/2 * K_gain[k][i][j] * n[i] * n[j]

    for i in range(GRID_RES):
        for j in range(GRID_RES):
            out += K_loss[k][i][j] * n[i] * n[j] * kronecker_delta(i, k)

    return out


@jit(nopython=True)
def forward_state(K_gain, K_loss, x, n):

    # Initialize mass-distribution derivative vector.
    dn = np.zeros(len(x))

    # Calulcate entries of derivative vector.
    for k, _ in enumerate(n):
        dn[k] = dn_k(K_gain, K_loss, n, k)
    return n + dn
