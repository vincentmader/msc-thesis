#!/usr/bin/env python3
import enum
import os

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from config import X_MIN, X_MAX, GRID_RESOLUTION
from config import PATH_TO_FIGURES
from config import DT, NR_OF_TIMESTEPS
from interactive_plot import interactive_plot


def gaussian(x, mu, sigma):
    return np.exp(-((x-mu)/sigma)**2) / ((2*np.pi)**.5 * sigma)


def initialize_state():
    x = np.linspace(X_MIN, X_MAX, GRID_RESOLUTION)
    n = np.array([0, 1] + [0] * (GRID_RESOLUTION-2))
    # n = gaussian(x, 3, 1)
    return x, n


def plot_state(t, x, n):
    # plt.bar(x, n)
    plt.plot(x, n, label=f"$t={t}$")
    plt.title("particle mass distribution")
    plt.xlabel("mass $x$")
    plt.ylabel("abundancy $n(x)$")
    plt.xlim(X_MIN-1, 10)  # X_MAX+1)


def save_plot():
    path = os.path.join(PATH_TO_FIGURES, "particle_mass_distribution.png")
    plt.savefig(path)


def K(x, y):
    # return 0.5
    return 1


def forward_state(t, x, n):
    dn = np.array([])
    for i, n_i in enumerate(n):
        # Determine contribution of associative processes.
        A = 1/2 * sum([K(i, j) * n[j] * n[i-j] for j in range(i)])
        # Determine contribution of disassociative processes.
        D = sum([K(i, j) * n_i * n_j for j, n_j in enumerate(n)])

        # if i == t+1:
        #     print(f"t={t}, x={i}, A={A}")
        #     print(f"t={t}, x={i}, D=-{D}")

        # Calculate total temporal derivative.
        dn = np.append(dn, A-D)
    # print(max(n))
    return n + dn * DT


def main():
    x, n0 = initialize_state()

    ns = [n0]
    for t in tqdm(range(NR_OF_TIMESTEPS)):
        plot_state(t, x, ns[-1])

        n_old = ns[t]
        n_new = forward_state(t, x, n_old)
        ns.append(n_new)

    plt.legend()
    save_plot()
    plt.show()


if __name__ == "__main__":
    main()
