import os

from datetime import datetime as dt
from numba import float64 as f64

from config import PATH_TO_DATA


def save_data(x, ns):
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
    path_to_savefile = os.path.join(
        path_to_savedir, "mass-distribution n(m).txt")

    # Save to file & return the name (so that plots are named the same).
    with open(path_to_savefile, 'w') as fp:
        fp.write(content)
    return run_id
