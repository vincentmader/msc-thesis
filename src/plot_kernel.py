import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np

from coagulation_kernel import K
from config import GRID_RESOLUTION

VMIN, VCEN, VMAX = -1, 0, 1
CMAP_NORM = colors.TwoSlopeNorm(vmin=VMIN, vcenter=VCEN, vmax=VMAX)


def plot_kernel(k):
    # Calculate entries of kernel at given k-value.
    kernel = np.zeros((GRID_RESOLUTION, GRID_RESOLUTION))
    for i in range(GRID_RESOLUTION):
        for j in range(GRID_RESOLUTION):
            kernel[i][j] = K(k, i, j)

    # Make sure that kernel is normalized to [-1, 1].
    # NOTE: Necessary for now, but is it also in general?
    if kernel.any() > 1 or kernel.any() < -1: 
        raise Exception("ERROR: Kernel is not normalized to [-1, 1].")

    # Create plot.
    plt.pcolor(kernel, norm=CMAP_NORM)
    plt.set_cmap("bwr")
    plt.colorbar()
    plt.xlabel("$i$")
    plt.ylabel("$j$")
    plt.show()
    plt.close()


if __name__ == "__main__":
    k = GRID_RESOLUTION / 2  # NOTE: This is an arbitrary choice.

    # Plot kernel.
    plot_kernel(k)
