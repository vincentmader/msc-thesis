import os

import matplotlib.pyplot as plt
import numpy as np

from config import PATH_TO_FIGURES, PATH_TO_DATA
from config import MPL_THEME, FIG_SIZE
from config import X_MIN, X_MAX
import utils

plt.style.use(MPL_THEME)


def plot_states(savefile_name, show_plot=False):
    # Load simulation-data from save-file into string.
    path_to_savefile = os.path.join(PATH_TO_DATA, f"{savefile_name}.txt")
    with open(path_to_savefile, 'r') as fp:
        content = fp.readlines()

    # Create figure.
    _ = plt.figure(figsize=FIG_SIZE)

    # Load x-vector from string.
    x = np.array([float(i) for i in content[0].split(",")])
    for t, line in enumerate(content[1:]):
        # Load n-vector from string.
        n = np.array([float(i) for i in line.split(",")])
        # Plot mass distribution n against mass x.
        plot_state(t, x, n)

    # Prettify plot.
    plt.title("particle mass distribution")
    plt.xlabel("mass $x$")
    plt.ylabel("abundancy $n(x)$")
    plt.xlim(X_MIN-1, X_MAX+1)  # X_MAX+1)
    plt.legend(loc="best")

    # Save plot to file.
    save_plot(savefile_name, show_plot=show_plot)


def plot_state(t, x, n):
    # Calculate total mass (to show together with time-step in plot-label).
    m_tot = utils.calc_total_mass(x, n)
    label = f"$t={t},\ M={m_tot}$"

    # Plot mass distribution.
    plt.plot(x, n, label=label)
    # plt.semilogx(x, n*x**2, label=label)
    # plt.bar(x, n, label=label)


def save_plot(savefile_name, show_plot=False):
    path = os.path.join(PATH_TO_FIGURES, f"{savefile_name}.png")
    plt.savefig(path)
    if show_plot is True:
        plt.show()
