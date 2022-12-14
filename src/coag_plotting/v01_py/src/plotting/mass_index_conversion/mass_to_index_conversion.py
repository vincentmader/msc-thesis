import os

import matplotlib.pyplot as plt
import numpy as np

from utils.mass_index_conversion import index_from_mass
from utils.cprint import cprint


def plot_mass_to_index_conversion(cfg):
    cprint("Plotting mass-to-index conversion...", indent=1)

    mass_grid_min_value = cfg.mass_grid_min_value
    mass_grid_max_value = cfg.mass_grid_max_value
    mass_grid_resolution = cfg.mass_grid_resolution

    masses = np.logspace(
        mass_grid_min_value, mass_grid_max_value, mass_grid_resolution
    )
    indices = np.array([index_from_mass(m, cfg) for m in masses])

    plt.figure(figsize=cfg.default_fig_size)
    plt.plot(masses, indices)
    plt.scatter(masses, indices, s=10)
    plt.title("Conversion from mass $m_i$ to index $i$")
    plt.xlabel("mass $m_i$")
    plt.ylabel("index $i$")

    # ax = plt.gca()
    # ax.set_xscale('log')

    filename = "mass-to-index conversion.png"
    path_to_savefile = os.path.join(cfg.path_to_outfiles, filename)
    plt.savefig(path_to_savefile)

    if "mass-index conversion" in cfg.plots_to_show:
        plt.show()
    plt.close()
