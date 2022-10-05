import os

import matplotlib.pyplot as plt

from config import PATH_TO_FIGURES
from config import X_MIN, X_MAX, GRID_RESOLUTION


def create_plot():
    plt.legend()


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
    plt.show()
