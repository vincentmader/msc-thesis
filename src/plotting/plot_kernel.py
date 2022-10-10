import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np

from config import GRID_RESOLUTION

VMIN, VCEN, VMAX = -1, 0, 1
CMAP_NORM = colors.TwoSlopeNorm(vmin=VMIN, vcenter=VCEN, vmax=VMAX)


def plot_kernel_layer(K, k, show_plot=False):
    # Make sure that kernel is normalized to [-1, 1].
    # NOTE: Necessary for now, but is it also in general?
    if K.any() > 1 or K.any() < -1:
        raise Exception("ERROR: Kernel is not normalized to [-1, 1].")

    # Create plot.
    plt.pcolor(K[k], norm=CMAP_NORM)
    plt.set_cmap("bwr")
    plt.colorbar()
    plt.xlabel("$j$")
    plt.ylabel("$i$")
    if show_plot:
        plt.show()
    plt.close()


def plot_kernel(K, run_id, show_plot=False, ks=range(GRID_RESOLUTION)):
    for k in ks:
        plot_kernel_layer(K, k, show_plot=show_plot)
