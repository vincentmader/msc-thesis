import json
import os

from numba import njit
import numpy as np


@njit
def zero_pad_int(num: int, nr_of_digits: int) -> str:
    out = str(num)
    while len(out) < nr_of_digits:
        out = f"0{out}"
    return out


def get_run_id(cfg):
    path_to_runs = os.path.join(cfg.path_to_outfiles, "runs")
    outfiles = os.listdir(path_to_runs)
    run_ids = [i for i in outfiles if i not in [".DS_Store"]]
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
    run_id = zero_pad_int(run_id, cfg.max_run_id_length)

    # date_str = dt.now().strftime("%Y-%m-%d")
    # time_str = dt.now().strftime("%H:%M:%S")
    # run_id = f"run-id={run_id}, date={date_str}, time={time_str}"
    run_id = f"id={run_id}"
    return run_id


# ─────────────────────────────────────────────────────────────────────────────


def save_run_info_to_file(cfg, run_id, timing_info):
    start = timing_info[0]
    end = timing_info[1]

    start_timestamp_in_mus = int(start.timestamp() * 1e6)
    end_timestamp_in_mus = int(end.timestamp() * 1e6)
    duration_in_mus = (end - start).microseconds

    info_file_content = f"start_timestamp_in_mus={start_timestamp_in_mus}\n"
    info_file_content += f"end_timestamp_in_mus={end_timestamp_in_mus}\n"
    info_file_content += f"duration_in_mus={duration_in_mus}"

    path_to_info_file = os.path.join(cfg.path_to_outfiles, "runs", run_id, "run_info.txt")
    with open(path_to_info_file, "w", encoding="utf-8") as fp:
        fp.write(info_file_content)


# ─────────────────────────────────────────────────────────────────────────────


def setup_savedir(cfg, run_id):
    # Define path to save-directory.
    path_to_savedir = os.path.join(cfg.path_to_outfiles, "runs", run_id)

    # Make sure that out-directory exists.
    os.system(f"mkdir -p \"{path_to_savedir}\"")

    return path_to_savedir


def setup_data_savedir(cfg, run_id):
    # Define path to save-directory.
    path_to_savedir = os.path.join(cfg.path_to_outfiles, "runs", run_id, "data")

    # Make sure that out-directory exists.
    os.system(f"mkdir -p \"{path_to_savedir}\"")

    return path_to_savedir


def setup_plot_savedir(cfg, run_id):
    # Define path to save-directory.
    path_to_savedir = os.path.join(cfg.path_to_outfiles, "runs", run_id, "figures")

    # Make sure that out-directory exists.
    os.system(f"mkdir -p \"{path_to_savedir}\"")

    return path_to_savedir


# ─────────────────────────────────────────────────────────────────────────────


def save_config(cfg, run_id):
    path_i = cfg.path_to_config
    path_f = os.path.join(cfg.path_to_outfiles, "runs", run_id, "config.toml")
    os.system(f"cp \"{path_i}\" \"{path_f}\"")


# ─────────────────────────────────────────────────────────────────────────────


def save_simulation_data(cfg, run_id, x, ns):
    # Define content of save-file.
    content = ",".join([str(i) for i in x]) + "\n"
    for n in ns:
        content += ",".join([str(i) for i in n]) + "\n"

    # Define (& create, if necessary) save-directory for simulation data.
    path_to_data_savedir = setup_data_savedir(cfg, run_id)

    # Define path to save-file.
    filename = "mass-distribution N(m).txt"
    path_to_savefile = os.path.join(path_to_data_savedir, filename)

    # Save to file & return run-id (so that plots can be named the same).
    with open(path_to_savefile, 'w', encoding="utf-8") as fp:
        fp.write(content)
    return run_id


def load_simulation_data(cfg, run_id):
    # Define path to save-file.
    filename = "mass-distribution N(m).txt"
    path_to_savefile = os.path.join(cfg.path_to_outfiles, "runs", run_id, "data", filename)

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


# ─────────────────────────────────────────────────────────────────────────────


def save_coagulation_kernel_to_file(cfg, run_id, K):
    # Define (& create, if necessary) save-directory for simulation data.
    path_to_data_savedir = setup_data_savedir(cfg, run_id)

    # Save gain-term of kernel to file.
    path_to_kernel = os.path.join(path_to_data_savedir, "kernel.txt")
    with open(path_to_kernel, "w", encoding="utf-8") as fp:
        json.dump(K.tolist(), fp)


def load_coagulation_kernel_from_file(cfg, run_id):
    path_to_data_savedir = setup_data_savedir(cfg, run_id)
    path_to_kernel = os.path.join(path_to_data_savedir, "kernel.txt")
    with open(path_to_kernel, "r", encoding="utf-8") as fp:
        K = json.load(fp)
    return np.array(K)


# ─────────────────────────────────────────────────────────────────────────────
