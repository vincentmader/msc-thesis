import os
import toml


def run_solver(solver_version="v01"):
    if solver_version == "v01":
        os.system("./venv/bin/python3 ./src/coag_solvers/v01_py/src/main.py")
    elif solver_version == "v02":
        os.system("cd ./src/coag_solvers/v02_rs && cargo run --release")
    else:
        raise Exception(f"Undefined solver-version: \"{solver_version}\"")


def run_plotter():
    os.system("./venv/bin/python3 ./src/coag_plotting/src/main.py")


if __name__ == "__main__":
    print("Running project...")
    cfg = toml.load("./config.toml")
    run_solver(solver_version=cfg["solver"]["version"])
    run_plotter()
