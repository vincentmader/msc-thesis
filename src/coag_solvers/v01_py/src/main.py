from tqdm import tqdm

import coagulation
from config import Config
import state_forwarding
import state_initialization
import utils
from utils.cprint import cprint


def run_solver(cfg, K, n0):
    mass_grid_exp_min = cfg.mass_grid_exp_min
    mass_grid_stepsize = cfg.mass_grid_stepsize
    run_stability_tests = cfg.run_stability_tests

    # Define vector holding mass-distributions for each time-step.
    ns = [n0]

    M_0 = utils.calc_total_mass(n0, mass_grid_exp_min, mass_grid_stepsize)
    dM, M = 0, M_0

    t_0 = 1
    t = t_0

    # Start forward-loop.
    for i_t in tqdm(range(cfg.nr_of_timesteps)):
        if run_stability_tests:
            print(f"\n\t{t=}", end="")

        if cfg.dt_incrementation == "additive":
            dt = cfg.additive_dt
        elif cfg.dt_incrementation == "multiplicative":
            dt = cfg.multiplicative_dt * t
        else:
            raise Exception

        # Load current mass-distribution.
        n_old = ns[i_t]
        # Calulcate new mass-distribution.
        n_new = state_forwarding.forward_state(
            K,
            n_old,
            mass_grid_exp_min,
            mass_grid_stepsize,
            run_stability_tests,
            dt,
        )
        # Append new mass-distribution to state-vector.
        ns.append(n_new)

        if run_stability_tests:
            M_tp1 = utils.calc_total_mass(
                ns[-1], mass_grid_exp_min, mass_grid_stepsize)
            dM = (M_tp1-M_0) / M_0*100
            print(f"\n\t\t(M_{t+1}-M_0)/M_0 = {dM:.2E} %")
            print(
                f"\t\t(M_{t+1}-M_{max(0,t)})/M_{max(0,t)} = {(M_tp1-M)/M*100:.2E} %\n\n\n\n\n\n")
            M = M_tp1

        t += dt

    cprint(f"- t_i = {t_0}", indent=1)
    cprint(f"- t_f = {t:.2E}", indent=1)

    return ns


def main():
    cprint("Running solver v01_py...", indent=1)

    # Load solver configuration from TOML file.
    cfg = Config()

    # Define coagulation kernel & initialize disk mass distribution.
    # ─────────────────────────────────────────────────────────────────────────

    K = coagulation.kernel.K(cfg)

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
            run_solver, *[cfg, K, n0]
        )
        start, end, duration = timing_info
        cprint(f"Execution time: {duration}", indent=1, color="green")

        # Create file containing information about this run.
        utils.file_io.save_run_info_to_file(cfg, run_id, timing_info)

        # Save mass distributions to file.
        utils.file_io.save_simulation_data(cfg, run_id, x, ns)

    # Save kernel(s) to file.
    utils.file_io.save_coagulation_kernel(cfg, run_id, K)


if __name__ == "__main__":
    main()
