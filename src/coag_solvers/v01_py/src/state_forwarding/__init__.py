import numpy as np
from numba import jit

from utils.elementary_functions import kronecker_delta


@jit(nopython=True)
def dn_k(K_gain, K_loss, n, k):
    res = 0

    mass_grid_resolution = K_gain.shape[0]

    for i in range(mass_grid_resolution):
        for j in range(mass_grid_resolution):
            res += K_gain[k][i][j] * n[i] * n[j]

    for i in range(mass_grid_resolution):
        for j in range(mass_grid_resolution):
            res += K_loss[k][i][j] * n[i] * n[j] * kronecker_delta(i, k)

    return res


@jit(nopython=True)
def forward_state(K_gain, K_loss, x, n):

    # Initialize mass-distribution derivative vector.
    dn = np.zeros(len(x))

    # Calulcate entries of derivative vector.
    for k, _ in enumerate(n):
        dn[k] = dn_k(K_gain, K_loss, n, k)

    return n + dn
