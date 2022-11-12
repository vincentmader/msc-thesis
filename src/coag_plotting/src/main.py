import os

from termcolor import colored
import matplotlib.pyplot as plt

from config import PLOTS_TO_CREATE
from config import RUNS_TO_PLOT
from config import GRID_RESOLUTION as GRID_RES
from config import MPL_THEME
from config import PATH_TO_OUTFILES
from plotting import plot_error_vs_time
from plotting.mass_index_conversion import mass_to_index_conversion
from plotting.mass_index_conversion import index_to_mass_conversion
from plotting import plot_kernel
from plotting import plot_mass_distribution_over_time
import utils


def get_run_ids():
    out = []
    path_to_runs = os.path.join(PATH_TO_OUTFILES, "runs")
    run_ids = os.listdir(path_to_runs)
    run_ids = sorted(run_ids)
    run_ids = [i for i in run_ids if i.startswith("id=")]
    if RUNS_TO_PLOT == "all":
        for run_id in run_ids:
            if run_id in [".DS_Store"]:
                continue
            out.append(run_id)
    elif RUNS_TO_PLOT == "last":
        out.append(run_ids[-1])
    else:
        raise Exception(f"ERROR: runs_to_plot \"{RUNS_TO_PLOT}\" is not defined.")
    return out


def main():
    print(colored("\nRunning plotter...", "yellow"))

    k = int(GRID_RES/2)
    ks = range(k, k+1)

    # Define matplotlib theme & apply (if specified in config).
    if MPL_THEME:
        plt.style.use(MPL_THEME)

    if "mass-index conversion" in PLOTS_TO_CREATE:
        mass_to_index_conversion.plot_mass_to_index_conversion()
        index_to_mass_conversion.plot_index_to_mass_conversion()

    run_ids = get_run_ids()
    for run_id in run_ids:
        print(colored(f"\tPlotting for {run_id}", "blue"))

        # Make sure the directory for saving plots exists.
        utils.file_io.setup_plot_savedir(run_id)

        # Plot the disk mass distribution over time.
        if "mass distribution" in PLOTS_TO_CREATE:
            plot_mass_distribution_over_time(run_id)

        # Plot the coagulation kernel.
        if "coagulation kernel" in PLOTS_TO_CREATE:
            plot_kernel(run_id, ks=ks)

        # Plot the relative error of the disk mass over time.
        if "mass error" in PLOTS_TO_CREATE:
            plot_error_vs_time(run_id)


if __name__ == "__main__":
    main()
