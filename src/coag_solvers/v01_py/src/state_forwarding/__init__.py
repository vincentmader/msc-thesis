import numpy as np
from numba import jit


@jit(nopython=True, cache=True)
def dn_k(K_gain, K_loss, n, k):
    dn_k = 0

    for i in range(len(n)):
        for j in range(len(n)):
            gain = 1/2 * K_gain[k][i][j] * n[i] * n[j]
            dn_k += gain

    for j, _ in enumerate(n):
        i = k
        loss = K_loss[k][i][j] * n[i] * n[j]
        dn_k += loss

    return dn_k


@jit(nopython=True, cache=True)
def forward_state(K_gain, K_loss, x, n):
    # Initialize mass-distribution derivative vector.
    dn = np.zeros(len(x))
    # Calulcate entries of derivative vector.
    for k, _ in enumerate(n):
        dn[k] = dn_k(K_gain, K_loss, n, k)
    return n + dn
