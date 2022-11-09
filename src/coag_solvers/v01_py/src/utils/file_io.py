from datetime import datetime as dt
import json
import os

import numpy as np

from config import PATH_TO_DATA, PATH_TO_FIGURES, PATH_TO_CONFIG


def get_run_id():
    run_ids = [i for i in os.listdir(PATH_TO_DATA) if i not in [".DS_Store"]]
    run_ids = sorted(run_ids, reverse=True)
    if len(run_ids) == 0:
        run_id = 0
    else:
        run_id = run_ids[0]
        run_id = run_id.split("=")
        run_id = run_id[1]
        run_id = run_id.split(",")
        run_id = run_id[0]
        run_id = int(run_id) + 1

    date_str = dt.now().strftime("%Y-%m-%d")
    time_str = dt.now().strftime("%H:%M:%S")
    run_id = f"run-id={run_id}, date={date_str}, time={time_str}"
    return run_id


def setup_data_savedir(run_id):
    # Define path to save-directory.
    path_to_savedir = os.path.join(PATH_TO_DATA, run_id)

    # Make sure that out-directory exists.
    os.mkdir(path_to_savedir)

    return path_to_savedir


def setup_plot_savedir(run_id):
    print("\t\tCreating directory for plots...")
    path = os.path.join(PATH_TO_FIGURES, run_id)
    os.system(f"mkdir -p \"{path}\"")


def save_simulation_data(run_id, x, ns):
    # Define content of save-file.
    content = ",".join([str(i) for i in x]) + "\n"
    for n in ns:
        content += ",".join([str(i) for i in n]) + "\n"

    # Define (& create, if necessary) save-directory for simulation data.
    path_to_data_savedir = setup_data_savedir(run_id)

    # Define path to save-file.
    filename = "mass-distribution N(m).txt"
    path_to_savefile = os.path.join(path_to_data_savedir, filename)

    # Save to file & return run-id (so that plots can be named the same).
    with open(path_to_savefile, 'w', encoding="utf-8") as fp:
        fp.write(content)
    return run_id


def save_coagulation_kernel(run_id, K_gain, K_loss):
    # Save gain-term of kernel to file.
    path_to_kernel = os.path.join(PATH_TO_DATA, run_id, "kernel_gain.txt")
    with open(path_to_kernel, "w", encoding="utf-8") as fp:
        json.dump(K_gain.tolist(), fp)

    # Save loss-term of kernel to file.
    path_to_kernel = os.path.join(PATH_TO_DATA, run_id, "kernel_loss.txt")
    with open(path_to_kernel, "w", encoding="utf-8") as fp:
        json.dump(K_loss.tolist(), fp)


def save_config(run_id):
    path_i = PATH_TO_CONFIG
    path_f = os.path.join(PATH_TO_DATA, run_id, "config.toml")
    os.system(f"cp \"{path_i}\" \"{path_f}\"")


def load_simulation_data(run_id):
    # Define path to save-file.
    filename = "mass-distribution N(m).txt"
    path_to_savefile = os.path.join(PATH_TO_DATA, run_id, filename)

    # Load file contents into string.
    with open(path_to_savefile, "r", encoding="utf-8") as fp:
        content = fp.readlines()

    # Load m-vector from string.
    m = np.array([float(i) for i in content[0].split(",")])

    # Load N-vector from string.
    Ns = []
    for line in content[1:]:
        N = np.array([float(i) for i in line.split(",")])
        Ns.append(N)

    return m, Ns
