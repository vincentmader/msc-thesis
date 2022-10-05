import os

import matplotlib.pyplot as plt

from config import PATH_TO_FIGURES
from config import X_MIN, X_MAX
import utils

plt.style.use('~/.config/matplotlib/dark.mplstyle')


def plot_state(t, x, n):
    m_tot = utils.calc_total_mass(x, n)
    label = f"$t={t},\ M={m_tot}$"

    # plt.bar(x, n, label=label)
    plt.plot(x, n, label=label)

    plt.title("particle mass distribution")
    plt.xlabel("mass $x$")
    plt.ylabel("abundancy $n(x)$")
    plt.xlim(X_MIN-1, X_MAX+1)  # X_MAX+1)
    plt.legend(loc="best")


def save_plot(show=False):
    path = os.path.join(PATH_TO_FIGURES, "particle_mass_distribution.png")
    plt.savefig(path)
    if show is True:
        plt.show()
