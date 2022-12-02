import os
import toml

from termcolor import colored
from utils.cprint import cprint
from utils.cprint import cprint_header


def create_coagulation_kernel(version="v01"):
    cprint(f"1. Creation of Coagulation Kernel", newline=True, color="blue")
    if version == "v01":
        os.system("./venv/bin/python3 ./src/coag_kernels/v01_py/src/main.py")
    elif version == "v02":
        os.system("cd ./src/coag_kernels/v02_rs && cargo run --release")
    else:
        error_msg = f"Undefined solver-version: \"{version}\""
        raise Exception(colored(error_msg, "red"))


def run_coagulation_solver(version="v01"):
    cprint(f"2. Execution of Coagulation Solver", newline=True, color="blue")
    if version == "v01":
        os.system("./venv/bin/python3 ./src/coag_solvers/v01_py/src/main.py")
    elif version == "v02":
        os.system("cd ./src/coag_solvers/v02_rs && cargo run --release")
    else:
        error_msg = f"Undefined solver-version: \"{version}\""
        raise Exception(colored(error_msg, "red"))


def run_plotter():
    cprint("3. Visualization of Results", newline=True, color="blue")
    os.system("./venv/bin/python3 ./src/coag_plotting/src/main.py")


if __name__ == "__main__":
    cprint_header()

    # Load configuration from TOML file.
    cfg = toml.load("./config.toml")

    # Run coagulation kernel creation subroutine.
    kernel_version = cfg["project"]["kernel_version"]
    create_coagulation_kernel(version=kernel_version)

    # Run coagulation solver.
    solver_version = cfg["project"]["solver_version"]
    run_coagulation_solver(version=solver_version)

    # Run python plotter.
    run_plotter()
