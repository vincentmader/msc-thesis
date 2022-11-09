import numpy as np
from numba import jit


@jit(nopython=True, cache=True)
def dn_k(K, n, k):
    dn_k = 0

    for i in range(len(n)):
        for j in range(len(n)):
            gain = 1/2 * K[k][i][j] * n[i] * n[j]
            dn_k += gain

    for j, _ in enumerate(n):
        i = k
        loss = K[k][i][j] * n[i] * n[j]
        dn_k += loss

    return dn_k


@jit(nopython=True, cache=True)
def forward_state(K, x, n):
    # Initialize mass-distribution derivative vector.
    dn = np.zeros(len(x))
    # Calulcate entries of derivative vector.
    for k, _ in enumerate(n):
        dn[k] = dn_k(K, n, k)
    return n + dn
