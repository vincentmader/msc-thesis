import os

from termcolor import colored

from config import Config
from utils.file_io import get_run_id
from utils.cprint import cprint
from utils.cprint import cprint_header


def create_coagulation_kernel(run_id, version="v01"):
    cprint(f"1. Creation of Coagulation Kernel", newline=True, color="blue")
    if version == "v01":
        file = "./src/coag_kernels/v01_py/src/main.py"
        os.system(f"./venv/bin/python3 {file} {run_id}")
    elif version == "v02":
        os.system("cd ./src/coag_kernels/v02_rs && cargo run --release")
    elif version == "v03":
        file = "./src/coag_kernels/v03_py_kees/src/main.py"
        os.system(f"./venv/bin/python3 {file} {run_id}")
    else:
        error_msg = f"Undefined solver-version: \"{version}\""
        raise Exception(colored(error_msg, "red"))


def run_coagulation_solver(run_id, version="v01"):
    cprint(f"2. Execution of Coagulation Solver", newline=True, color="blue")
    if version == "v01":
        os.system(
            f"./venv/bin/python3 ./src/coag_solvers/v01_py/src/main.py {run_id}")
    elif version == "v02":
        os.system("cd ./src/coag_solvers/v02_rs && cargo run --release")
    else:
        error_msg = f"Undefined solver-version: \"{version}\""
        raise Exception(colored(error_msg, "red"))


def run_plotter(run_id):
    cprint("3. Visualization of Results", newline=True, color="blue")
    os.system(f"./venv/bin/python3 ./src/coag_plotting/v01_py/src/main.py {run_id}")


if __name__ == "__main__":
    cprint_header()

    # Load configuration from TOML file.
    cfg = Config()
    run_id = get_run_id(cfg)

    # Run coagulation kernel creation subroutine.
    kernel_version = cfg.kernel_version
    create_coagulation_kernel(run_id, version=kernel_version)

    # Run coagulation solver.
    solver_version = cfg.solver_version
    run_coagulation_solver(run_id, version=solver_version)

    # Run python plotter.
    run_plotter(run_id)
