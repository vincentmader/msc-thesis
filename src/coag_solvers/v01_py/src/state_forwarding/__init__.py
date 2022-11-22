import numpy as np
from numba import njit

from utils.mass_index_conversion import mass_from_index


@njit()
def dn_k(K, n, k):
    dn_k = 0
    for i in range(K.shape[1]):
        for j in range(K.shape[2]):
            dn_k += K[k][i][j] * n[i] * n[j]
    return dn_k


@njit()
def forward_state(
    K,
    x,
    n,
    mass_grid_exp_min,
    mass_grid_stepsize,
    run_stability_tests,
):
    # Initialize mass-distribution derivative vector.
    dn = np.zeros(len(x))

    # Calulcate entries of derivative vector.
    for k, _ in enumerate(n):
        dn[k] = dn_k(K, n, k)

    if run_stability_tests:
        dmdt = sum([
            n_k * mass_from_index(k, mass_grid_exp_min, mass_grid_stepsize)
            for k, n_k in enumerate(dn)
        ])
        print("\n\t\tSum_k dn_k/dt = dm/dt =", dmdt)
    return n + dn
