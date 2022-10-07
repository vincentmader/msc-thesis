#!/usr/bin/env python3
from numba import jit
import numpy as np
from tqdm import tqdm

from config import DT, NR_OF_TIMESTEPS
import initialization
import plotting
import utils
from coagulation_kernel import coagulation_kernel as K


@jit(nopython=True, cache=True)
def forward_state(t, x, n):
    dn = np.empty(len(x))
    for i, n_i in enumerate(n):
        # Determine contribution of assoc. & disassoc. processes, respectively.
        A = 1/2 * sum([K(i, j) * n[j] * n[i-j] for j in range(i)])
        D = sum([K(i, j) * n_i * n_j for j, n_j in enumerate(n)])
        # Calculate total temporal derivative.
        dn[i] = A - D
    return n + dn*DT


def run(x, n0):
    ns = [n0]
    for t in tqdm(range(NR_OF_TIMESTEPS)):
        # Plot current state.
        plotting.plot_state(t, x, ns[-1])
        # Forward state to next time-step.
        ns.append(forward_state(t, x, ns[t]))
    return ns


if __name__ == "__main__":
    # Instantiate initial state.
    x, n0 = initialization.get_initial_state()

    # Start forward-loop.
    ns, _ = utils.record_execution_time(run, *[x, n0])

    # Save (& show) plot.
    plotting.save_plot(show=True)
    utils.save_data(x, ns)
