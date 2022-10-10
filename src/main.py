#!/usr/bin/env python3
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
    run_id = utils.save_data(x, ns)

    # Create, save (& show) plots.
    plotting.plot_states(run_id, show_plot=True)
    #   plotting.plot_kernel(K, run_id, show_plot=True)


if __name__ == "__main__":
    main()
