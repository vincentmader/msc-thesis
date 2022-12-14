import os

import matplotlib.pyplot as plt
import numpy as np

from utils.mass_index_conversion import mass_from_index
from utils.cprint import cprint


def plot_index_to_mass_conversion(cfg):
    cprint("Plotting index-to-mass conversion...", indent=1)

    mass_grid_resolution = cfg.mass_grid_resolution

    indices = np.arange(0, mass_grid_resolution + 1, 1)
    masses = np.array([mass_from_index(i, cfg) for i in indices])

    plt.figure(figsize=cfg.default_fig_size)
    plt.plot(indices, masses)
    plt.scatter(indices, masses, s=10)
    plt.title("Conversion from index $i$ to mass $m_i$")
    plt.xlabel("index $i$")
    plt.ylabel("mass $m_i$")

    # ax = plt.gca()
    # ax.set_yscale('log')

    filename = "index-to-mass conversion.png"
    path_to_savefile = os.path.join(cfg.path_to_outfiles, filename)
    plt.savefig(path_to_savefile)

    if "mass-index conversion" in cfg.plots_to_show:
        plt.show()
    plt.close()
