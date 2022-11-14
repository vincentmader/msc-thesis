import os

from termcolor import colored
import matplotlib.pyplot as plt

from config import Config
from plotting import plot_error_vs_time
from plotting.mass_index_conversion import mass_to_index_conversion
from plotting.mass_index_conversion import index_to_mass_conversion
from plotting import plot_kernel
from plotting import plot_mass_distribution_over_time
import utils


def get_run_ids(cfg):
    out = []
    path_to_runs = os.path.join(cfg.path_to_outfiles, "runs")
    run_ids = os.listdir(path_to_runs)
    run_ids = sorted(run_ids)
    run_ids = [i for i in run_ids if i.startswith("id=")]
    if cfg.runs_to_plot == "all":
        for run_id in run_ids:
            if run_id in [".DS_Store"]:
                continue
            out.append(run_id)
    elif cfg.runs_to_plot == "last":
        out.append(run_ids[-1])
    else:
        raise Exception(f"ERROR: runs_to_plot \"{cfg.runs_to_plot}\" is not defined.")
    return out


def main(cfg):
    print(colored("\nRunning plotter...", "yellow"))

    k = int(cfg.mass_grid_resolution/2)
    ks = range(k, k+1)

    # Define matplotlib theme & apply (if specified in config).
    if cfg.mpl_theme:
        plt.style.use(cfg.mpl_theme)

    if "mass-index conversion" in cfg.plots_to_create:
        mass_to_index_conversion.plot_mass_to_index_conversion(cfg)
        index_to_mass_conversion.plot_index_to_mass_conversion(cfg)

    run_ids = get_run_ids(cfg)
    for run_id in run_ids:
        print(colored(f"\tPlotting for {run_id}", "blue"))

        # Make sure the directory for saving plots exists.
        utils.file_io.setup_plot_savedir(cfg, run_id)

        if cfg.run_solver:
            # Plot the disk mass distribution over time.
            if "mass distribution" in cfg.plots_to_create:
                plot_mass_distribution_over_time(cfg, run_id)

            # Plot the relative error of the disk mass over time.
            if "mass error" in cfg.plots_to_create:
                plot_error_vs_time(cfg, run_id)

        # Plot the coagulation kernel.
        if "coagulation kernel" in cfg.plots_to_create:
            plot_kernel(cfg, run_id, ks)


if __name__ == "__main__":
    # Load configuration TOML file.
    cfg = Config()
    
    # Start plotter.
    main(cfg)
