#!/usr/bin/env python3
from datetime import datetime as dt
import enum
import os

import matplotlib.pyplot as plt
from numpy.typing import NDArray
import numba
from numba import float64 as f64
from numba import jit
import numpy as np
from tqdm import tqdm

from config import X_MIN, X_MAX, GRID_RESOLUTION
from config import PATH_TO_FIGURES
from config import DT, NR_OF_TIMESTEPS


def gaussian(x, mu, sigma) -> f64[:]:
    y = np.exp(-((x-mu)/sigma)**2) / ((2*np.pi)**.5 * sigma)
    return y


def dirac_delta(x, i_x0) -> f64[:]:
    # y = np.zeros(len(x))
    # y[i_x0] = 1
    # return y
    return np.array([0, 1] + [0] * (GRID_RESOLUTION-2))


def record_execution_time(f):
    start = dt.now()
    res = f()
    end = dt.now()
    duration = (end - start)
    return duration, res


def initialize_state() -> f64[:]:
    x = np.linspace(X_MIN, X_MAX, GRID_RESOLUTION)
    n: numba.float64[:] = np.array([0, 1] + [0] * (GRID_RESOLUTION-2))
    # n = gaussian(x, 3, 1)
    return x, n


def plot_state(t, x, n):
    plt.style.use('~/.config/matplotlib/dark.mplstyle')
    # plt.bar(x, n)
    plt.plot(x, n, label=f"$t={t}$")
    plt.title("particle mass distribution")
    plt.xlabel("mass $x$")
    plt.ylabel("abundancy $n(x)$")
    plt.xlim(X_MIN-1, 10)  # X_MAX+1)


def save_plot():
    path = os.path.join(PATH_TO_FIGURES, "particle_mass_distribution.png")
    plt.savefig(path)

# =============================================================================


@jit(nopython=True)
def K(x, y):
    return 1  # 0.5


@jit(nopython=True)
def empty(N):
    return np.empty(N, f64)


# @jit(nopython=True, parallel=True, cache=True)
@jit(nopython=True)
def forward_state(t, x, n):
    dn: f64[:] = empty(len(x))
    for i, n_i in enumerate(n):
        # Determine contribution of associative & disassociative processes, respectively.
        A: f64 = 1/2 * sum([K(i, j) * n[j] * n[i-j] for j in range(i)])
        D: f64 = sum([K(i, j) * n_i * n_j for j, n_j in enumerate(n)])
        # Calculate total temporal derivative.
        dn[i] = A-D
    return n + dn*DT


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
    # plt.show()


if __name__ == "__main__":
    d, r = record_execution_time(main)

    print(d)
