import matplotlib.pyplot as plt

from config import FIG_SIZE, STEPS_BETWEEN_PLOT
from config import GRID_EXP_MIN, GRID_EXP_MAX
import utils


def plot_mass_distribution_over_time(run_id, show_plot=False):
    # Load simulation-data from save-file into string.
    m, Ns = utils.file_io.load_simulation_data(run_id)

    # Calculate total mass in the disk at t=0.
    M_0 = utils.calc_total_mass(m, Ns[0])

    # Create figure.
    _ = plt.figure(figsize=FIG_SIZE)

    # Plot mass distribution n against mass x for several points in time.
    for t, N in enumerate(Ns):
        if t % STEPS_BETWEEN_PLOT != 0:
            continue
        plot_mass_distribution(t, m, N, M_0)

    # Prettify plot.
    plt.title("particle mass distribution")
    plt.xlabel("particle mass $m$")
    plt.ylabel("abundancy $m\cdot N(m)$")
    plt.legend(loc="upper right")
    plt.xlim(10**GRID_EXP_MIN, 10**GRID_EXP_MAX)
    plt.ylim(10**(-9), 10**(-3))

    # Save plot to file.
    utils.file_io.save_plot(run_id, show_plot=show_plot)


def plot_mass_distribution(t, m, N, M_0):
    # Calculate total mass (to show together with time-step in plot-label).
    M = utils.calc_total_mass(m, N)

    # Calculate relative mass error with respect to initial disk mass.
    err = round((M / M_0 - 1) * 100, 2)

    # Define label: Show time, & area under curve (i.e. total mass).
    a = 2*" " if t != 0 else 6*" "
    b = r"\Delta M/M_0"
    c = err
    label = f"${t=}$,{a}${b}={c}$ %"

    # Plot mass distribution.
    plt.loglog(m, N*m, label=label)
