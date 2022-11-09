import os

import matplotlib.pyplot as plt

from config import NR_OF_TIMESTEPS, PATH_TO_OUTFILES, PLOTS_TO_SHOW
import utils


def plot_error_vs_time(run_id, save_plot=True):
    print("\t\tPlotting error vs. time...")

    # Load simulation-data from save-file into string.
    m, Ns = utils.file_io.load_simulation_data(run_id)
    # Define time-axis.
    t = range(NR_OF_TIMESTEPS)

    # Calculate total mass in the disk at various times.
    M = [utils.calc_total_mass(m, Ns[t]) for t in t]
    # Calculate relative error.
    err = [(M[t] / M[0] - 1) * 100 for t in t]

    # Create new figure.
    _ = plt.figure()
    # Plot error vs. time.
    plt.plot(t, err)
    # Define axis-labels.
    plt.title("Relative error of total disk-mass over time")
    plt.xlabel("time $t$")
    plt.ylabel(r"relative error $\frac{\Delta M}{M_0}$ [%]")

    # Decide whether to show the plot.
    show_plot = "mass error" in PLOTS_TO_SHOW
    # Show plot (optional).
    if show_plot is True:
        plt.show()
    # Save plot to file.
    if save_plot:
        save_plot_to_file(run_id)

    # Close the figure to save RAM.
    plt.close()


def save_plot_to_file(run_id):
    filename = "total-disk-mass relative-error.png"
    path_to_savefile = os.path.join(PATH_TO_OUTFILES, run_id, "figures", filename)
    plt.savefig(path_to_savefile)
