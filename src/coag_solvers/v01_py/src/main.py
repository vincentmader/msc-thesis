from tqdm import tqdm
from termcolor import colored

import coagulation
from config import Config
import state_initialization
import state_forwarding
import utils


def run_solver(
    cfg, 
    K_gain, 
    K_loss, 
    x, 
    n0, 
    mass_grid_exp_min,
    mass_grid_stepsize,
    run_stability_tests,
):
    # Define vector holding mass-distributions for each time-step.
    ns = [n0]

    M_0 = utils.calc_total_mass(x, n0, mass_grid_exp_min, mass_grid_stepsize)
    dM, M = 0, M_0

    # Start forward-loop.
    # for t in tqdm(range(cfg.nr_of_timesteps)):
    for t in range(cfg.nr_of_timesteps):
        print(f"\n\t{t=}", end="")
        # Load current mass-distribution.
        n_old = ns[t]
        # Calulcate new mass-distribution & append to state vector.
        n_new = state_forwarding.forward_state(
            K_gain, 
            K_loss, 
            x, 
            n_old, 
            mass_grid_exp_min, 
            mass_grid_stepsize,
            run_stability_tests,
        )
        ns.append(n_new)

        M_tp1 = utils.calc_total_mass(x, ns[-1], mass_grid_exp_min, mass_grid_stepsize)
        dM = (M_tp1-M_0) / M_0*100
        print(f"\n\t\t(M_{t+1}-M_0)/M_0 = {round(dM,2)} %")
        print(f"\t\t(M_{t+1}-M_{max(0,t-1)})/M_{max(0,t-1)} = {round((M_tp1-M)/M*100, 2)} %")
        M = M_tp1

    print()
    return ns


def main():
    print(colored("\nRunning solver v01_py...", "yellow"))

    # Load solver configuration from TOML file.
    cfg = Config()

    # Define coagulation kernel & initialize disk mass distribution.
    # ─────────────────────────────────────────────────────────────────────────

    K_gain, K_loss = coagulation.kernel.K(
        cfg.mass_grid_resolution,
        cfg.mass_grid_exp_min,
        cfg.mass_grid_stepsize,
        cfg.coagulation_kernel_variant,
        cfg.run_stability_tests,
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
        # Compute evolution of mass distribution & record execution duration.
        ns, timing_info = utils.record_execution_time(
            run_solver, *[
                cfg,
                K_gain,
                K_loss,
                x,
                n0,
                cfg.mass_grid_exp_min,
                cfg.mass_grid_stepsize,
                cfg.run_stability_tests,
            ]
        )

        # Create file containing information about this run.
        utils.file_io.save_run_info_to_file(cfg, run_id, timing_info)

        # Save mass distributions to file.
        utils.file_io.save_simulation_data(cfg, run_id, x, ns)

    # Save kernel(s) to file.
    K = K_gain - K_loss
    utils.file_io.save_coagulation_kernel(cfg, run_id, K)


if __name__ == "__main__":
    main()
