import numpy as np
from numba import jit

from config import GRID_RESOLUTION as GRID_RES
from utils.elementary_functions import kronecker_delta
from utils.mass_index_conversion import mass_from_index, index_from_mass


@jit(nopython=True)
def dn_k(K_gain, K_loss, n, k):
    res = 0
    
    i_max = GRID_RES  # i_max = index_from_mass(mass_from_index(k) / 2)
    for i in range(i_max):
        for j in range(GRID_RES):
            res += 1/2 * K_gain[k][i][j] * n[i] * n[j]

    for i in range(GRID_RES):
        for j in range(GRID_RES):
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
