import json
import os

import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np

VMIN, VCEN, VMAX = -1, 0, 1
CMAP_NORM = colors.TwoSlopeNorm(vmin=VMIN, vcenter=VCEN, vmax=VMAX)


def plot_kernel_layer(cfg, K, run_id, k, show_plot=False, save_plot=True):
    # Make sure that kernel is normalized to [-1, 1].
    # NOTE: Necessary for now, but is it also in general?
    if K.any() > 1 or K.any() < -1:
        raise Exception("ERROR: Kernel is not normalized to [-1, 1].")

    # Create plot.
    _ = plt.figure()
    plt.title("$K_{kij}$ " + "for $k={}$".format(k))
    plt.pcolor(K[k], norm=CMAP_NORM)
    plt.set_cmap("bwr")
    plt.colorbar()
    plt.xlabel("$j$")
    plt.ylabel("$i$")

    # Save plot (optional).
    if save_plot:
        save_plot_to_file(cfg, run_id, k)

    # Show plot (optional).
    if show_plot:
        plt.show()  # NOTE: Showing before saving may lead to corrupted plot file!

    # Close the figure to save RAM.
    plt.close()


def plot_kernel(cfg, run_id, ks):
    print("\t\tPlotting kernel...")

    path_to_kernel = os.path.join(cfg.path_to_outfiles, "runs", run_id, "data", "kernel_gain.txt")
    with open(path_to_kernel, encoding="utf-8") as fp:
        K_gain = np.array(json.load(fp))
    path_to_kernel = os.path.join(cfg.path_to_outfiles, "runs", run_id, "data", "kernel_loss.txt")
    with open(path_to_kernel, encoding="utf-8") as fp:
        K_loss = np.array(json.load(fp))
    K = K_gain + K_loss

    path = os.path.join(cfg.path_to_outfiles, "runs", run_id, "figures", "kernel")
    os.system(f"mkdir -p \"{path}\"")

    # Decide whether to show the plot.
    show_plot = "coagulation kernel" in cfg.plots_to_show

    for k in ks:
        plot_kernel_layer(cfg, K, run_id, k, show_plot=show_plot)


def save_plot_to_file(cfg, run_id, k):
    filename = f"kernel K_kij with {k=}.png"
    path_to_savefile = os.path.join(
        cfg.path_to_outfiles, "runs", run_id, "figures", "kernel", filename
    )
    plt.savefig(path_to_savefile)
