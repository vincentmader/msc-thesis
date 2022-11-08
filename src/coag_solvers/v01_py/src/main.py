from tqdm import tqdm

import coagulation
from config import NR_OF_TIMESTEPS
import state_initialization
import state_forwarding
import utils


def run(K_gain, K_loss, x, n0):
    # Define vector holding mass-distributions for each time-step.
    ns = [n0]

    # Start forward-loop.
    for t in tqdm(range(NR_OF_TIMESTEPS)):
        # Load current mass-distribution.
        n_old = ns[t]

        # Calulcate new mass-distribution.
        n_new = state_forwarding.forward_state(K_gain, K_loss, x, n_old)

        # Append to vector.
        ns.append(n_new)
    return ns


def main():
    print("Running solver v01_py...")

    # Define initial state.
    x, n0 = state_initialization.initial_state()
    # Define coagulation kernel (gain & loss term, separately).
    K_gain = coagulation.kernel.K_gain()
    K_loss = coagulation.kernel.K_loss()

    # Run forward-loop & get time-evolution of mass distribution.
    ns, _ = utils.record_execution_time(run, *[K_gain, K_loss, x, n0])

    # Define this simulation's run-ID.
    run_id = utils.file_io.get_run_id()
    # Save mass distributions to file.
    utils.file_io.save_simulation_data(run_id, x, ns)
    # Save kernel(s) to file.
    utils.file_io.save_coagulation_kernel(run_id, K_gain, K_loss)
    # Copy over configuration file (for reference later on).
    utils.file_io.save_config(run_id)


if __name__ == "__main__":
    main()
