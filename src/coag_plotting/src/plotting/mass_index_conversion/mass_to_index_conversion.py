import os

import matplotlib.pyplot as plt
import numpy as np

from utils.mass_index_conversion import index_from_mass
from utils.cprint import cprint


def plot_mass_to_index_conversion(cfg):
    cprint("Plotting mass-to-index conversion...", indent=1)

    mass_grid_exp_min = cfg.mass_grid_exp_min
    mass_grid_exp_max = cfg.mass_grid_exp_max
    mass_grid_resolution = cfg.mass_grid_resolution
    mass_grid_stepsize = cfg.mass_grid_stepsize

    masses = np.logspace(
        mass_grid_exp_min, mass_grid_exp_max, mass_grid_resolution)
    indices = np.array([
        index_from_mass(m, mass_grid_exp_min, mass_grid_stepsize) for m in masses
    ])

    plt.figure(figsize=cfg.default_fig_size)
    plt.plot(masses, indices)
    plt.scatter(masses, indices, s=10)
    plt.title("Conversion from mass $m_i$ to index $i$")
    plt.xlabel("mass $m_i$")
    plt.ylabel("index $i$")

    filename = "mass-to-index conversion.png"
    path_to_savefile = os.path.join(cfg.path_to_outfiles, filename)
    plt.savefig(path_to_savefile)

    if "mass-index conversion" in cfg.plots_to_show:
        plt.show()
    plt.close()
