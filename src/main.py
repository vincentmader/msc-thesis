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

        # TODO: remove factor 1/2 from assoc. contribution.
        # A_2 = sum([K(i, j) * n[j] * n[i-j] for j in range(i/2)])
        # A_2 = sum([K(i, j) * n[j] * n[i-j] for j in range(i/2+1)])
        # A_2 = sum([K(i, j) * n[j] * n[i-j] for j in range(int(i/2))])
        # A_2 = sum([K(i, j) * n[j] * n[i-j] for j in range(int(i/2)+1)])
        # if A != A_2:
        #     print(i, "\t", A, A_2)

        # Calculate total temporal derivative.
        dn[i] = A-D
    return n + dn*DT


def main():
    # Define initial state.
    x, n0 = initialization.initialize_state()
    ns = [n0]
    # Start forward-loop.
    for t in tqdm(range(NR_OF_TIMESTEPS)):
        # Plot current state.
        plotting.plot_state(t, x, ns[-1])
        # Forward state to next time-step.
        ns.append(forward_state(t, x, ns[t]))
    # Save (& show) plot.
    plotting.save_plot(show=True)


if __name__ == "__main__":
    duration, _ = utils.record_execution_time(main)
    print(f"\nExecution time: {duration}")
