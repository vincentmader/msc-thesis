import os
import toml


def run_solver(version="v01"):
    # Handle solver v01 (written in Python).
    if version == "v01":
        # Use virtual environment to execute Python solver.
        os.system("./venv/bin/python3 ./src/coag_solvers/v01_py/src/main.py")

    # Handle solver v02 (written in Rust).
    elif version == "v02":
        # Navigate to v02 directory & execute Rust solver.
        os.system("cd ./src/coag_solvers/v02_rs && cargo run --release")

    # Raise exception if solver version is not defined.
    else:
        raise Exception(f"Undefined solver-version: \"{version}\"")


def run_plotter():
    # Execute Python plotter.
    os.system("./venv/bin/python3 ./src/coag_plotting/src/main.py")


if __name__ == "__main__":
    # Load configuration from TOML file.
    cfg = toml.load("./config.toml")

    # Load solver version from configuration.
    solver_version = cfg["solver"]["version"]

    # Run coagulation solver (either written in Python or Rust).
    run_solver(version=solver_version)

    # Run python plotter.
    run_plotter()
