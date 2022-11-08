import os

import json
from tqdm import tqdm

import coagulation
from config import NR_OF_TIMESTEPS, PATH_TO_DATA
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

    # Define coagulation kernel.
    K_gain = coagulation.kernel.K_gain()
    K_loss = coagulation.kernel.K_loss()

    # Run forward-loop & get time-evolution of mass distribution.
    ns, _ = utils.record_execution_time(run, *[K_gain, K_loss, x, n0])

    # Save mass distributions to file.
    # Also, define this simulation-run's ID, which will
    # be used for the filename of the output-plot as well.
    run_id = utils.file_io.save_simulation_data(x, ns)

    # Save gain-term of kernel to file.
    path_to_kernel = os.path.join(PATH_TO_DATA, run_id, "kernel_gain.txt")
    with open(path_to_kernel, "w") as fp:
        json.dump(K_gain.tolist(), fp)

    # Save loss-term of kernel to file.
    path_to_kernel = os.path.join(PATH_TO_DATA, run_id, "kernel_loss.txt")
    with open(path_to_kernel, "w") as fp:
        json.dump(K_loss.tolist(), fp)


if __name__ == "__main__":
    main()
