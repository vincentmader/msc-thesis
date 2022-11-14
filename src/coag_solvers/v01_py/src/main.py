from numpy import test
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

        # Calulcate new mass-distribution & append to state vector.
        n_new = state_forwarding.forward_state(K_gain, K_loss, x, n_old)
        ns.append(n_new)

    return ns


def test_mass_conservation(cfg, K_gain, K_loss):
    i = 0
    j = 0
    m_i = utils.mass_from_index(i, cfg.mass_grid_exp_min, cfg.mass_grid_stepsize)
    m_j = utils.mass_from_index(j, cfg.mass_grid_exp_min, cfg.mass_grid_stepsize)
    print("m_i =", m_i)
    print("m_j =", m_j)

    m = m_i + m_j
    k_l = utils.index_from_mass(m, cfg.mass_grid_exp_min, cfg.mass_grid_stepsize)
    k_h = k_l + 1
    print("k_l =", k_l)
    print("k_h =", k_h)

    m_l = utils.mass_from_index(k_l, cfg.mass_grid_exp_min, cfg.mass_grid_stepsize)
    m_h = utils.mass_from_index(k_h, cfg.mass_grid_exp_min, cfg.mass_grid_stepsize)

    eps = (m_i + m_j - m_l) / (m_h - m_l)
    print("eps =", eps)

    a = m_i * K_gain[k_l][i][j] + m_j * K_gain[k_h][i][j]
    b = (m_i + m_j) *  K_loss[i][i][j]
    if a != b:
        print()
        print(a)
        print(b)
        if b == -2*a:
            print("There is (at least) a factor 1/2 error here!")


def main():
    print(colored("\nRunning solver v01_py...", "yellow"))

    # Load solver configuration from TOML file.
    cfg = Config()

    # Define coagulation kernel & initialize disk mass distribution.
    # ─────────────────────────────────────────────────────────────────────────

    # Define coagulation kernel (gain & loss terms, separately).
    K_gain, K_loss = coagulation.kernel.K(
        cfg.mass_grid_resolution,
        cfg.mass_grid_exp_min,
        cfg.mass_grid_stepsize,
        cfg.coagulation_kernel_variant
    )
    test_mass_conservation(cfg, K_gain, K_loss)

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
            run_solver, *[cfg, K_gain, K_loss, x, n0]
        )

        # Create file containing information about this run.
        utils.file_io.save_run_info_to_file(cfg, run_id, timing_info)

        # Save mass distributions to file.
        utils.file_io.save_simulation_data(cfg, run_id, x, ns)

    # Save kernel(s) to file.
    utils.file_io.save_coagulation_kernel(cfg, run_id, K_gain, K_loss)


if __name__ == "__main__":
    main()
