import os

import matplotlib.pyplot as plt

import utils
from utils.cprint import cprint


def plot_mass_distribution_over_time(cfg, run_id):
    cprint("Plotting mass distribution...", indent=1)
    # Load simulation-data from save-file into string.
    m, Ns = utils.file_io.load_simulation_data(cfg, run_id)

    # Calculate total mass in the disk at t=0.
    M_0 = utils.calc_total_mass(Ns[0], cfg)

    # Create figure.
    _ = plt.figure(figsize=cfg.default_fig_size)

    # Plot mass distribution n against mass x for several points in time.
    for t, N in enumerate(Ns):
        if t % cfg.steps_between_plot != 0:
            continue
        plot_mass_distribution(cfg, t, m, N, M_0)

    # Prettify plot.
    plt.title("particle mass distribution")
    plt.xlabel("particle mass $m$")
    plt.ylabel("particle abundancy $m\cdot N(m)$")
    plt.legend(loc="upper right", ncol=2)
    plt.xlim(cfg.mass_grid_min, cfg.mass_grid_max)
    y_max = max([max(m*N) for N in Ns]) * 1e3
    y_min = y_max / 1e9
    plt.ylim(y_min, y_max)

    # Save plot to file.
    save_plot_to_file(cfg, run_id)

    # Decide whether to show the plot.
    show_plot = "mass distribution" in cfg.plots_to_show
    # Show the plot (optional).
    if show_plot is True:
        plt.show()

    # Make sure pyplot does not fill up RAM with unclosed figures.
    plt.close()


def plot_mass_distribution(cfg, t, m, N, M_0):
    # Calculate total mass (to show together with time-step in plot-label).
    M = utils.calc_total_mass(N, cfg)

    # Calculate relative mass error with respect to initial disk mass.
    err = (M / M_0 - 1) * 100

    # Define label: Show time, & area under curve (i.e. total mass).
    if t == 0:
        a = 7*" "
    elif t == 1000:
        a = " "
    else:
        a = 3*" "
    # a = 2*" " if t != 0 else 6*" "
    b = r"\Delta M/M_0"
    c = f"{err:.1e}"
    c = c if err < 0 else f" {c}"
    label = f"$i_t={t}$,{a}${b}=${c} %"

    # Plot mass distribution.
    plt.loglog(m, N*m, label=label)


def save_plot_to_file(cfg, run_id):
    # Define path to file that plot should be written to.
    filename = "mass-distribution N(m).png"
    path_to_savefile = os.path.join(
        cfg.path_to_outfiles, "runs", run_id, "figures", filename)

    # Save the figure.
    plt.savefig(path_to_savefile)
