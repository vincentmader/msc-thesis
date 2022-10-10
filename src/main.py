#!/usr/bin/env python3
import numpy as np
from numpy import float64 as f64
from numba import jit
from tqdm import tqdm

import initialization
import plotting
import utils
from coagulation_kernel import K_gain, K_loss
from config import NR_OF_TIMESTEPS


@jit(nopython=True, cache=True)
def dn_k(n, k):
    G, L = 0, 0
    for i, _ in enumerate(n):
        for j, _ in enumerate(n):
            # Calculate gain-term contribution.
            G += K_gain(k, i, j) * n[i] * n[j]
            # Calculate loss-term contribution.
            L += K_loss(k, i, j) * n[i] * n[j]
    return G - L


@jit(nopython=True, cache=True)
def forward_state(t, x, n):
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
        n_new = forward_state(t, x, n_old)
        # Append to vector.
        ns.append(n_new)
    return ns


if __name__ == "__main__":
    # Instantiate initial state.
    x, n0 = initialization.get_initial_state()
    # Run forward-loop & get time-evolution of mass distribution.
    ns, _ = utils.record_execution_time(run, *[x, n0])
    # Save mass distributions to file.
    savefile_name = utils.save_data(x, ns)
    # Create, save (& show) plot(s).
    plotting.plot_states(savefile_name, show_plot=True)
