import matplotlib.pyplot as plt

import config
import utils

def plot_error_vs_time(run_id, show_plot=False):
    # Load simulation-data from save-file into string.
    m, Ns = utils.file_io.load_simulation_data(run_id)

    # Define time-axis.
    t = range(config.NR_OF_TIMESTEPS)

    # Calculate total mass in the disk at various times.
    M = [utils.calc_total_mass(m, Ns[t]) for t in t]

    # Calculate relative error.
    err = [(M[t] / M[0] - 1) * 100 for t in t]

    # Plot error vs. time.
    plt.plot(t, err)

    # Define axis-labels.
    plt.title("Relative error of total disk-mass over time")
    plt.xlabel("time $t$")
    plt.ylabel(r"relative error $\frac{\Delta M}{M_0}$ [%]")

    # Show plot (optional).
    if show_plot is True:
        plt.show()
