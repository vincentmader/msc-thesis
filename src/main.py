#!/usr/bin/env python3
import os

import matplotlib.pyplot as plt
import numpy as np

from config import X_MIN, X_MAX, GRID_RESOLUTION
from config import PATH_TO_FIGURES


def initialize_state():
    x = np.linspace(X_MIN, X_MAX, GRID_RESOLUTION)
    n = np.array([1] + [0] * (GRID_RESOLUTION-1))
    return x, n


def plot_state(x, n):
    plt.bar(x, n)
    plt.title("particle mass distribution")
    plt.xlabel("mass $x$")
    plt.ylabel("abundancy $n(x)$")
    plt.xlim(X_MIN-1, X_MAX+1)
    path = os.path.join(PATH_TO_FIGURES, "particle_mass_distribution.png")
    plt.savefig(path)
    plt.show()


def main():
    x, n0 = initialize_state()
    plot_state(x, n0)


if __name__ == "__main__":
    main()
