import matplotlib.pyplot as plt
import os

import numpy as np
from numba import njit


@njit()
def dndt_k(K, n, k):
    dndt_k = 0

    for i in range(K.shape[1]):
        for j in range(K.shape[2]):
            dndt_k += K[k][i][j] * n[i] * n[j]

    return dndt_k


@njit()
def forward_state(K, n, dt):

    # Initialize mass-distribution derivative vector.
    dn = np.zeros(len(n))

    # Calulcate entries of derivative vector.
    for k, _ in enumerate(n):
        dn[k] = dndt_k(K, n, k) * dt

    # plt.figure()
    # plt.plot(dn / n)
    # # plt.ylim(1e-40, 1e30)
    # # path = os.path.join(cfg.path_to_outfiles, "test", f"N(t={i_t}).png")
    # # plt.savefig(path)
    # plt.show()
    # plt.close()

    # if run_stability_tests:
        # dmdt = sum([
        #     n_k * mass_from_index(k, cfg)
        #     for k, n_k in enumerate(dn)
        # ])
        # print("\n\t\tSum_k dn_k/dt = dm/dt =", dmdt)

    return n + dn
