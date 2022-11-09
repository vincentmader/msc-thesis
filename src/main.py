import os
import toml


def run_solver(solver_version="v01"):
    # Handle solver version 01 (writte in Python).
    if solver_version == "v01":
        os.system("./venv/bin/python3 ./src/coag_solvers/v01_py/src/main.py")

    # Handle solver version 02 (written in Rust).
    elif solver_version == "v02":
        os.system("cd ./src/coag_solvers/v02_rs && cargo run --release")

    # Raise exception if solver version is not defined.
    else:
        raise Exception(f"Undefined solver-version: \"{solver_version}\"")


def run_plotter():
    os.system("./venv/bin/python3 ./src/coag_plotting/src/main.py")


if __name__ == "__main__":
    # Load configuration file.
    cfg = toml.load("./config.toml")

    # Run coagulation solver (either written in Python or Rust).
    run_solver(solver_version=cfg["solver"]["version"])
    # Run python plotter.
    run_plotter()
