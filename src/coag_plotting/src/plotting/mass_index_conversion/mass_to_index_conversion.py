import os

import matplotlib.pyplot as plt
import numpy as np

from config import FIG_SIZE
from config import PLOTS_TO_SHOW
from config import PATH_TO_OUTFILES
from config import GRID_RESOLUTION as GRID_RES
from config import GRID_EXP_MIN
from config import GRID_EXP_MAX
from utils.mass_index_conversion import index_from_mass


def plot_mass_to_index_conversion():
    print("\tPlotting mass-to-index conversion...")

    masses = np.logspace(GRID_EXP_MIN, GRID_EXP_MAX, GRID_RES)
    indices = np.array([index_from_mass(m) for m in masses])

    plt.figure(figsize=FIG_SIZE)
    plt.plot(masses, indices)
    plt.scatter(masses, indices, s=10)
    plt.title("Conversion from mass $m_i$ to index $i$")
    plt.xlabel("mass $m_i$")
    plt.ylabel("index $i$")

    filename = "mass-to-index conversion.png"
    path_to_savefile = os.path.join(PATH_TO_OUTFILES, filename)
    plt.savefig(path_to_savefile)

    if "mass-index conversion" in PLOTS_TO_SHOW:
        plt.show()
    plt.close()
