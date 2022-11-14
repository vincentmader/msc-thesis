import os
import toml

from termcolor import colored


def run_coagulation_solver(version="v01"):
    # Run solver-v01 from python virtual environment.
    if version == "v01":
        os.system("./venv/bin/python3 ./src/coag_solvers/v01_py/src/main.py")

    # Run solver-v02 (written in Rust).
    elif version == "v02":
        os.system("cd ./src/coag_solvers/v02_rs && cargo run --release")

    # Raise exception if solver version is undefined.
    else:
        error_msg = f"Undefined solver-version: \"{version}\""
        raise Exception(colored(error_msg, "red"))


def run_plotter():
    # Execute plotter from python virtual environment.
    os.system("./venv/bin/python3 ./src/coag_plotting/src/main.py")


if __name__ == "__main__":
    # Load configuration from TOML file.
    cfg = toml.load("./config.toml")

    # Extract solver-version from configuration.
    solver_version = cfg["solver"]["version"]

    # Run coagulation solver.
    run_coagulation_solver(version=solver_version)

    # Run python plotter.
    run_plotter()
