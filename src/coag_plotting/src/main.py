import os

from termcolor import colored
import matplotlib.pyplot as plt

from config import PATH_TO_OUTFILES, GRID_RESOLUTION, MPL_THEME, CREATE_PLOTS_FOR
from plotting import plot_error_vs_time
from plotting import plot_kernel
from plotting import plot_mass_distribution_over_time
import utils


def get_run_ids():
    out = []
    run_ids = sorted(os.listdir(PATH_TO_OUTFILES))
    run_ids = [i for i in run_ids if i.startswith("run-id=")]
    if CREATE_PLOTS_FOR == "all":
        for run_id in run_ids:
            if run_id in [".DS_Store"]:
                continue
            out.append(run_id)
    elif CREATE_PLOTS_FOR == "last":
        out.append(run_ids[-1])
    else:
        raise Exception(f"ERROR: plot_which_runs \"{CREATE_PLOTS_FOR}\" is not defined.")
    return out


def main():
    print(colored("\nRunning plotter...", "yellow"))

    k = int(GRID_RESOLUTION/2)
    ks = range(k, k+1)

    # Define matplotlib theme & apply (if specified in config).
    if MPL_THEME:
        plt.style.use(MPL_THEME)

    run_ids = get_run_ids()
    for run_id in run_ids:
        print(colored(f"\tPlotting for {run_id}", "blue"))

        # Make sure the directory for saving plots exists.
        utils.file_io.setup_plot_savedir(run_id)

        # Plot the disk mass distribution over time.
        plot_mass_distribution_over_time(run_id)

        # Plot the coagulation kernel.
        plot_kernel(run_id, ks=ks)

        # Plot the relative error of the disk mass over time.
        plot_error_vs_time(run_id)


if __name__ == "__main__":
    main()
