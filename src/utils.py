from datetime import datetime as dt
import os

import numpy as np
from numba import jit
from numba import float64 as f64

from config import PATH_TO_DATA


def gaussian(x, mu, sigma):
    y = np.exp(-((x-mu)/sigma)**2) / ((2*np.pi)**.5 * sigma)
    return y


def dirac_delta(x, i_x0):
    y = np.zeros(len(x))
    y[i_x0] = 1
    return y


@jit(nopython=True)
def kronecker_delta(i, j):
    return 1 if i == j else 0


def record_execution_time(f, *args):
    start = dt.now()
    res = f(*args)
    end = dt.now()
    duration = (end - start)
    print(f"\nExecution time: {duration}")
    return res, duration


def calc_total_mass(x, n):
    m_tot = sum(x_i * n_i for x_i, n_i in zip(x, n))
    return m_tot


def save_data(x, ns):
    # Define content of save-file.
    content = ",".join([str(i) for i in x]) + "\n"
    for n in ns:
        content += ",".join([str(i) for i in n]) + "\n"

    # Define name of save-file.
    sim_id = len([i for i in os.listdir(PATH_TO_DATA) if i.endswith(".txt")])
    time_str = dt.now().strftime("%Y-%m-%d_%H:%M:%S")
    filename = f"simulation_{sim_id}_from_{time_str}"

    # Define path to save-file.
    path_to_savefile = os.path.join(PATH_TO_DATA, f"{filename}.txt")

    # Save to file & return the name (so that plots are named the same).
    with open(path_to_savefile, 'w') as fp:
        fp.write(content)
    return filename
