import numpy as np
from numba import jit

from utils.elementary_functions import kronecker_delta
from utils.mass_index_conversion import mass_from_index


@jit(nopython=True)
def dn_k(K_gain, K_loss, n, k):
    dn_k = 0

    # Determine positive contribution to derivative from coagulation kernel's gain-term.
    for i in range(k+1):
        for j in range(k+1):
            dn_k += 1/2 * K_gain[k][i][j] * n[i] * n[j]
    # Determine negative contribution to derivative from coagulation kernel's loss-term.
    for i in range(K_loss.shape[0]):
        for j in range(K_loss.shape[0]):
            dn_k -= K_loss[k][k][j] * n[i] * n[j] * kronecker_delta(k, i)

    # for i in range(K_loss.shape[0]):
    #     for j in range(K_loss.shape[0]):
    #         K = 1/2 * K_gain[k][i][j] - K_loss[k][k][j] * kronecker_delta(k, i)
    #         dn_k += K * n[i] * n[j]

    return dn_k


@jit(nopython=True)
def forward_state(
    K_gain,
    K_loss,
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
        dn[k] = dn_k(K_gain, K_loss, n, k)

    if run_stability_tests:
        dmdt = sum([
            n_k * mass_from_index(k, mass_grid_exp_min, mass_grid_stepsize)
            for k, n_k in enumerate(dn)
        ])
        print("\n\t\tSum_k dn_k/dt = dm/dt =", dmdt)
    return n + dn
