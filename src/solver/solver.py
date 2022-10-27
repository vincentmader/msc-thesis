import numpy as np
from numba import jit
from tqdm import tqdm

from config import NR_OF_TIMESTEPS


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


def run(K_gain, K_loss, x, n0):
    # Define vector holding mass-distributions for each time-step.
    ns = [n0]

    # Start forward-loop.
    for t in tqdm(range(NR_OF_TIMESTEPS)):
        # Load current mass-distribution.
        n_old = ns[t]
        # Calulcate new mass-distribution.
        n_new = forward_state(K_gain, K_loss, x, n_old)
        # Append to vector.
        ns.append(n_new)
    return ns
