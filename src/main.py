#!/usr/bin/env python3
import numpy as np
from numba import jit
from tqdm import tqdm

import initialization
import plotting
import utils
from coagulation_kernel import coagulation_kernel as K
from config import DT, NR_OF_TIMESTEPS


def run(x, n0):
    ns = [n0]
    for t in tqdm(range(NR_OF_TIMESTEPS)):
        n_old = ns[t]
        n_new = forward_state(t, x, n_old)
        ns.append(n_new)
    return ns


@jit(nopython=True, cache=True)
def forward_state(t, x, n):
    # Initialize mass-distribution vector.
    dn = np.empty(len(x))
    for i, n_i in enumerate(n):
        # Determine contribution of assoc. & disassoc. processes, respectively.
        A = 1/2 * sum([K(i, j) * n[j] * n[i-j] for j in range(i)])
        D = sum([K(i, j) * n_i * n_j for j, n_j in enumerate(n)])
        # Calculate total temporal derivative.
        dn[i] = A - D
    return n + dn*DT


if __name__ == "__main__":
    # Instantiate initial state.
    x, n0 = initialization.get_initial_state()

    # Run forward-loop & get time-evolution of mass distribution.
    ns, _ = utils.record_execution_time(run, *[x, n0])

    # Save mass distributions to file.
    savefile_name = utils.save_data(x, ns)

    # Create, save (& show) plot(s).
    plotting.plot_states(savefile_name, show_plot=True)
