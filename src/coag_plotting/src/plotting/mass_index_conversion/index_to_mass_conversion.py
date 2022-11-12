import os

import matplotlib.pyplot as plt
import numpy as np

from config import FIG_SIZE
from config import PLOTS_TO_SHOW
from config import PATH_TO_OUTFILES
from config import GRID_RESOLUTION as GRID_RES
from utils.mass_index_conversion import mass_from_index


def plot_index_to_mass_conversion():
    print("\tPlotting index-to-mass conversion...")

    indices = np.arange(0, GRID_RES+1, 1)
    masses = np.array([mass_from_index(i) for i in indices])

    plt.figure(figsize=FIG_SIZE)
    plt.plot(indices, masses)
    plt.scatter(indices, masses, s=10)
    plt.title("Conversion from index $i$ to mass $m_i$")
    plt.xlabel("index $i$")
    plt.ylabel("mass $m_i$")

    filename = "index-to-mass conversion.png"
    path_to_savefile = os.path.join(PATH_TO_OUTFILES, filename)
    plt.savefig(path_to_savefile)

    if "mass-index conversion" in PLOTS_TO_SHOW:
        plt.show()
    plt.close()
