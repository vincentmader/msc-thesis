#!/usr/bin/env python3
import os 

from config import PATH_TO_FIGURES, GRID_RESOLUTION as GRES
import initialization
import plotting
import utils
import solver


def main():
    # Define initial state.
    x, n0 = initialization.initial_state()

    # Define coagulation kernel.
    K = solver.coagulation_kernel.create_coagulation_kernel()
    # K = solver.coagulation_kernel.create_coagulation_kernel_2()

    # Run forward-loop & get time-evolution of mass distribution.
    ns, _ = utils.record_execution_time(solver.run, *[K, x, n0])

    # Save mass distributions to file.
    # Also, define this simulation-run's ID, which will
    # be used for the filename of the output-plot as well.
    run_id = utils.file_io.save_simulation_data(x, ns)

    # Define path to directory where plots should be saved to.
    path_to_savedir = os.path.join(PATH_TO_FIGURES, run_id)
    # Make sure the save-directory exists.
    os.mkdir(path_to_savedir)

    # Create, save (& show) plots.
    plotting.plot_mass_distribution_over_time(run_id, show_plot=True)
    plotting.plot_kernel(K, run_id, show_plot=True, ks=[int(GRES/2)])
    plotting.plot_error_vs_time(run_id, show_plot=True)


if __name__ == "__main__":
    main()
