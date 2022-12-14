import os

import matplotlib.pyplot as plt

import utils
from utils.cprint import cprint


def save_plot_to_file(cfg, run_id):
    # Define path to file that plot should be written to.
    filename = "mass-distribution N(m).png"
    path_to_savefile = os.path.join(
        cfg.path_to_outfiles, "runs", run_id, "figures", filename)

    # Save the figure.
    plt.savefig(path_to_savefile)


def get_x_limits(cfg):
    min_value = cfg.mass_grid_min_value
    max_value = cfg.mass_grid_max_value
    if cfg.mass_grid_variant == "logarithmic":
        x_min = 10**min_value
        x_max = 10**max_value
    elif cfg.mass_grid_variant == "linear":
        x_min = min_value
        x_max = max_value
    else:
        raise Exception()
    return x_min, x_max


def get_y_limits(cfg, m, Ns):
    if cfg.mass_grid_variant == "logarithmic":
        y_max = max([max(m*N) for N in Ns]) * 1e3
        y_min = y_max / 1e9
    elif cfg.mass_grid_variant == "linear":
        y_min = 0
        y_max = 1
    else:
        raise Exception()
    if cfg.initial_mass_distribution == "flat":
        y_min = None
        y_max = None
    return y_min, y_max


def plot_mass_distribution(cfg, t, m, N, M_0):
    # Calculate total mass (to show together with time-step in plot-label).
    M = utils.calc_total_mass(N, cfg)

    # Calculate relative mass error with respect to initial disk mass.
    err = (M / M_0 - 1)

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
    label = f"$i_t={t}$,{a}${b}=${c}"

    # Plot mass distribution.
    if cfg.mass_grid_variant == "logarithmic":
        plt.loglog(m, N*m, label=label)
    elif cfg.mass_grid_variant == "linear":
        plt.plot(m, N, label=label)


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

    x_min, x_max = get_x_limits(cfg)
    y_min, y_max = get_y_limits(cfg, m, Ns)

    # Prettify plot.
    plt.title("particle mass distribution")
    plt.xlabel("particle mass $m$")
    plt.ylabel(r"particle abundancy $m\cdot N(m)$")
    if None not in [x_min, x_max]:
        plt.xlim(x_min, x_max)
    if None not in [y_min, y_max]:
        plt.ylim(y_min, y_max)

    plt.legend(loc="upper right", ncol=2)

    # Save plot to file.
    save_plot_to_file(cfg, run_id)

    # Decide whether to show the plot.
    show_plot = "mass distribution" in cfg.plots_to_show
    if show_plot is True:
        plt.show()

    # Make sure pyplot does not fill up RAM with unclosed figures.
    plt.close()
