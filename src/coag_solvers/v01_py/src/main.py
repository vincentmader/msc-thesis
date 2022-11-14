from tqdm import tqdm
from termcolor import colored

import coagulation
from config import Config
import state_initialization
import state_forwarding
import utils


def run_solver(cfg, K_gain, K_loss, x, n0):
    # Define vector holding mass-distributions for each time-step.
    ns = [n0]

    # Start forward-loop.
    for t in tqdm(range(cfg.nr_of_timesteps)):
        # Load current mass-distribution.
        n_old = ns[t]

        # Calulcate new mass-distribution.
        n_new = state_forwarding.forward_state(K_gain, K_loss, x, n_old)

        # Append to vector.
        ns.append(n_new)
    return ns


def main():
    print(colored("\nRunning solver v01_py...", "yellow"))

    # Load solver configuration from TOML file.
    cfg = Config()

    # Define coagulation kernel & initialize disk's mass distribution.
    # ─────────────────────────────────────────────────────────────────────────

    # Define coagulation kernel (gain & loss terms, separately).
    K_gain, K_loss = coagulation.kernel.K(
        cfg.mass_grid_resolution,
        cfg.mass_grid_exp_min,
        cfg.mass_grid_stepsize,
        cfg.coagulation_kernel_variant
    )

    # Define initial state.
    x, n0 = state_initialization.initial_state(cfg)

    # Setup file/directory structure.
    # ─────────────────────────────────────────────────────────────────────────

    # Define this simulation's run-ID.
    run_id = utils.file_io.get_run_id(cfg)

    # Make sure save-directory exists.
    utils.file_io.setup_savedir(cfg, run_id)

    # Copy over configuration file (for reference later on).
    utils.file_io.save_config(cfg, run_id)

    # Run coagulation solver
    # ─────────────────────────────────────────────────────────────────────────

    if cfg.run_solver:

        # Compute time-evolution of mass distribution .
        # Also, record execution duration.
        ns, timing_info = utils.record_execution_time(
            run_solver, *[cfg, K_gain, K_loss, x, n0]
        )

        # Create info file:
        # This file contains
        # - start- & end-datetime, as well as 
        # - execution duration.
        utils.file_io.save_run_info_to_file(cfg, run_id, timing_info)

        # Save mass distributions to file.
        utils.file_io.save_simulation_data(cfg, run_id, x, ns)

    # Save to file.
    # ─────────────────────────────────────────────────────────────────────────

    # Save kernel(s) to file.
    utils.file_io.save_coagulation_kernel(cfg, run_id, K_gain, K_loss)

if __name__ == "__main__":
    main()
