import matplotlib.pyplot as plt

from config import FIG_SIZE, STEPS_BETWEEN_PLOT
from config import GRID_EXP_MIN, GRID_EXP_MAX
import utils


def plot_states(run_id, show_plot=False):
    # Load simulation-data from save-file into string.
    m, Ns = utils.file_io.load_simulation_data(run_id)

    # Create figure.
    _ = plt.figure(figsize=FIG_SIZE)

    for t, N in enumerate(Ns):
        if t % STEPS_BETWEEN_PLOT != 0:
            continue
        # Plot mass distribution n against mass x.
        plot_state(t, m, N)

    # Prettify plot.
    plt.title("particle mass distribution")
    plt.xlabel("particle mass $m$")
    plt.ylabel("abundancy $m\cdot N(m)$")
    plt.legend(loc="upper right")
    plt.xlim(10**GRID_EXP_MIN, 10**GRID_EXP_MAX)
    plt.ylim(10**(-9), 10**(-3))

    # Save plot to file.
    utils.file_io.save_plot(run_id, show_plot=show_plot)


def plot_state(t, m, N):
    # Calculate total mass (to show together with time-step in plot-label).
    m_tot = utils.calc_total_mass(m, N)

    # Define label: Show time, & area under curve (i.e. total mass).
    label = f"$t={t},\ M={m_tot}$"

    # Plot mass distribution.
    plt.loglog(m, N*m, label=label)
