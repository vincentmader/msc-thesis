import os

import matplotlib.pyplot as plt
import numpy as np

from config import FIG_SIZE
from config import PATH_TO_FIGURES, PATH_TO_DATA
from config import X_MIN, X_MAX
import utils


def plot_states(run_id, show_plot=False):
    # Load simulation-data from save-file into string.
    path_to_savefile = os.path.join(
        PATH_TO_DATA, run_id, "mass-distribution n(m).txt")
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
    plt.xlim(X_MIN-1, X_MAX+1)
    plt.legend(loc="best")

    # Save plot to file.
    save_plot(run_id, show_plot=show_plot)


def plot_state(t, x, n):
    # Calculate total mass (to show together with time-step in plot-label).
    m_tot = utils.calc_total_mass(x, n)
    m_tot = round(m_tot, 3)
    label = f"$t={t},\ M={m_tot}$"

    # Plot mass distribution.
    plt.semilogx(x, n*x**2, label=label)
    # plt.plot(x, n, label=label)
    # plt.bar(x, n, label=label)


def save_plot(run_id, show_plot=False):
    # Define path to directory where plots should be saved to.
    path_to_savedir = os.path.join(PATH_TO_FIGURES, run_id)
    # Make sure the save-directory exists.
    os.mkdir(path_to_savedir)
    # Define path to file that plot should be written to.
    path_to_savefile = os.path.join(
        path_to_savedir, "mass-distribution n(m).png")
    # Save the figure.
    plt.savefig(path_to_savefile)
    # Show the plot (optional).
    if show_plot is True:
        plt.show()
    # Make sure pyplot does not fill up RAM with unclosed figures.
    plt.close()
