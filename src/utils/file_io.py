from datetime import datetime as dt
import os

import matplotlib.pyplot as plt
from numba import float64 as f64
import numpy as np

from config import PATH_TO_DATA
from config import PATH_TO_FIGURES


def save_simulation_data(x, ns):
    # Define content of save-file.
    content = ",".join([str(i) for i in x]) + "\n"
    for n in ns:
        content += ",".join([str(i) for i in n]) + "\n"

    # Define name of save-file.
    run_id = len([i for i in os.listdir(PATH_TO_DATA) if i.endswith(".txt")])
    date_str = dt.now().strftime("%Y-%m-%d")
    time_str = dt.now().strftime("%H:%M:%S")
    run_id = f"run-id={run_id}, date={date_str}, time={time_str}"

    # Define path to save-directory.
    path_to_savedir = os.path.join(PATH_TO_DATA, run_id)

    # Make sure that out-directory exists.
    os.mkdir(path_to_savedir)

    # Define path to save-file.
    filename = "mass-distribution N(m).txt"
    path_to_savefile = os.path.join(path_to_savedir, filename)

    # Save to file & return run-id (so that plots can be named the same).
    with open(path_to_savefile, 'w') as fp:
        fp.write(content)
    return run_id


def load_simulation_data(run_id):
    # Define path to save-file.
    filename = "mass-distribution N(m).txt"
    path_to_savefile = os.path.join(PATH_TO_DATA, run_id, filename)

    # Load file contents into string.
    with open(path_to_savefile, 'r') as fp:
        content = fp.readlines()

    # Load m-vector from string.
    m = np.array([float(i) for i in content[0].split(",")])

    # Load N-vector from string.
    Ns = []
    for line in content[1:]:
        N = np.array([float(i) for i in line.split(",")])
        Ns.append(N)

    return m, Ns


