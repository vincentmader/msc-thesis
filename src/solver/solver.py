import numpy as np
from numba import jit
from tqdm import tqdm

from config import NR_OF_TIMESTEPS
from .coagulation_kernel import K


@jit(nopython=True, cache=True)
def dn_k(n, k):
    dn_k = 0
    for i, _ in enumerate(n):
        for j, _ in enumerate(n):
            dn_k += K(k, i, j) * n[i] * n[j]
    return dn_k


@jit(nopython=True, cache=True)
def forward_state(x, n):
    # Initialize mass-distribution derivative vector.
    dn = np.zeros(len(x))
    # Calulcate entries of derivative vector.
    for k in range(len(n)):
        dn[k] = dn_k(n, k)
    return n + dn


def run(x, n0):
    # Define vector holding mass-distributions for each time-step.
    ns = [n0]
    # Start forward-loop.
    for t in tqdm(range(NR_OF_TIMESTEPS)):
        # Load current mass-distribution.
        n_old = ns[t]
        # Calulcate new mass-distribution.
        n_new = forward_state(x, n_old)
        # Append to vector.
        ns.append(n_new)
    return ns
