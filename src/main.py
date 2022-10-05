#!/usr/bin/env python3
from numba import jit
import numpy as np
from tqdm import tqdm

from config import X_MIN, X_MAX, GRID_RESOLUTION
from config import DT, NR_OF_TIMESTEPS
import utils
import plotting


def initialize_state():
    x = np.linspace(X_MIN, X_MAX, GRID_RESOLUTION)
    n = utils.dirac_delta(x, 1)
    return x, n


@jit(nopython=True)
def K(x, y):
    return 1  # 0.5


# @jit(nopython=True, parallel=True, cache=True)
@jit(nopython=True)
def forward_state(t, x, n):
    dn = np.empty(len(x))
    for i, n_i in enumerate(n):
        # Determine contribution of associative & disassociative processes, respectively.
        A = 1/2 * sum([K(i, j) * n[j] * n[i-j] for j in range(i)])
        D = sum([K(i, j) * n_i * n_j for j, n_j in enumerate(n)])
        # Calculate total temporal derivative.
        dn[i] = A-D
    return n + dn*DT


def main():
    # Define initial state.
    x, n0 = initialize_state()
    ns = [n0]
    # Start forward-loop.
    for t in tqdm(range(NR_OF_TIMESTEPS)):
        # Plot current state.
        plotting.plot_state(t, x, ns[-1])
        # Forward state to next time-step.
        ns.append(forward_state(t, x, ns[t]))
    # Save (& show) plot.
    plotting.save_plot()


if __name__ == "__main__":
    duration, _ = utils.record_execution_time(main)
    print(f"Execution time: {duration}")
