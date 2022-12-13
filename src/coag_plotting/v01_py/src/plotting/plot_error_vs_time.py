import os

import matplotlib.pyplot as plt

import utils
from utils.cprint import cprint


def plot_error_vs_time(cfg, run_id, save_plot=True):
    cprint("Plotting error vs. time...", indent=1)

    # Load simulation-data from save-file into string.
    _m, Ns = utils.file_io.load_simulation_data(cfg, run_id)
    # Define time-axis.
    t = range(cfg.nr_of_timesteps)

    # Calculate total mass in the disk at various times.
    M = [utils.calc_total_mass(Ns[t], cfg) for t in t]

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

    # Save plot to file.
    if save_plot:
        save_plot_to_file(cfg, run_id)

    # Decide whether to show the plot.
    show_plot = "mass error" in cfg.plots_to_show
    # Show plot (optional).
    if show_plot is True:
        plt.show()

    # Close the figure to save RAM.
    plt.close()


def save_plot_to_file(cfg, run_id):
    filename = "total-disk-mass relative-error.png"
    path_to_savefile = os.path.join(
        cfg.path_to_outfiles, "runs", run_id, "figures", filename)
    plt.savefig(path_to_savefile)
