import numpy as np
from numba import jit


@jit(nopython=True, cache=True)
def dn_k(K_gain, K_loss, n, k):
    out = 0

    for i, _ in enumerate(n):
        for j, _ in enumerate(n):
            gain = 1/2 * K_gain[k][i][j] * n[i] * n[j]
            out += gain

    for j, _ in enumerate(n):
        i = k
        loss = K_loss[k][i][j] * n[i] * n[j]
        out += loss

    return out


@jit(nopython=True, cache=True)
def forward_state(K_gain, K_loss, x, n):

    # Initialize mass-distribution derivative vector.
    dn = np.zeros(len(x))

    # Calulcate entries of derivative vector.
    for k, _ in enumerate(n):
        dn[k] = dn_k(K_gain, K_loss, n, k)
    return n + dn
