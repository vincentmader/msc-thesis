import os

import matplotlib.colors as colors
import matplotlib.pyplot as plt

from config import GRID_RESOLUTION, PATH_TO_FIGURES

VMIN, VCEN, VMAX = -1, 0, 1
CMAP_NORM = colors.TwoSlopeNorm(vmin=VMIN, vcenter=VCEN, vmax=VMAX)


def plot_kernel_layer(K, run_id, k, show_plot=False, save_plot=True):
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

    # Show plot (optional).   
    if show_plot:
        plt.show()  # NOTE: Showing before saving may lead to corrupted plot file!

    # Save plot (optional).
    if save_plot:
        save_plot_to_file(run_id, k)

    # Close the figure to save RAM.
    plt.close(run_id)


def plot_kernel(K, run_id, show_plot=False, ks=range(GRID_RESOLUTION)):
    for k in ks:
        plot_kernel_layer(K, run_id, k, show_plot=show_plot)


def save_plot_to_file(run_id, k):
    filename = f"kernel K_kij with {k=}.png"
    path_to_savefile = os.path.join(PATH_TO_FIGURES, run_id, filename)
    plt.savefig(path_to_savefile)
