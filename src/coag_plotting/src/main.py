import os

import matplotlib.pyplot as plt

from config import PATH_TO_DATA, PATH_TO_FIGURES, GRID_RESOLUTION
import plotting


def get_run_ids():
    out = []
    run_ids = os.listdir(PATH_TO_DATA)
    for run_id in run_ids:
        if run_id in [".DS_Store"]:
            continue
        out.append(run_id)
    return sorted(out)


def create_plot_dir(run_id):
    print("\t\tCreating directory for plots...")
    path = os.path.join(PATH_TO_FIGURES, run_id)
    os.system(f"mkdir -p \"{path}\"")


def main():
    print("Running plotter...")

    k = int(GRID_RESOLUTION/2)
    ks = range(k, k+1)

    # Define matplotlib theme & apply.
    MPL_THEME = "~/.config/matplotlib/dark.mplstyle"
    plt.style.use(MPL_THEME)

    run_ids = get_run_ids()
    for run_id in run_ids:
        print(f"\tPlotting for {run_id}")
        create_plot_dir(run_id)
        plotting.plot_mass_distribution_over_time(run_id)
        plotting.plot_kernel(run_id, ks=ks)
        plotting.plot_error_vs_time(run_id)


if __name__ == "__main__":
    main()
