#!/usr/bin/env python3
import initialization
import plotting
import utils
import solver

def main():
    # Define initial state.
    x, n0 = initialization.initial_state()

    # Run forward-loop & get time-evolution of mass distribution.
    ns, _ = utils.record_execution_time(solver.run, *[x, n0])

    # Save mass distributions to file.
    run_id = utils.save_data(x, ns)

    # Create, save (& show) plot(s).
    plotting.plot_states(run_id, show_plot=True)
    plotting.plot_kernel(run_id, show_plot=True)


if __name__ == "__main__":
    main()
