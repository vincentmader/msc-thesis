import numpy as np
from numba import jit


@jit(nopython=True)
def dn_k(K, n, k):
    res = 0
    for i in range(k+1):
        for j in range(K.shape[0]):
            res += K[k][i][j] * n[i] * n[j]
    return res


@jit(nopython=True)
def forward_state(K, x, n):
    # Initialize mass-distribution derivative vector.
    dn = np.zeros(len(x))

    # Calulcate entries of derivative vector.
    for k, _ in enumerate(n):
        dn[k] = dn_k(K, n, k)
    return n + dn
