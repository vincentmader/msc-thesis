import numpy as np

from config import X_MIN, X_MAX, GRID_RESOLUTION
import utils


def initialize_state():
    x = np.linspace(X_MIN, X_MAX, GRID_RESOLUTION)
    n = utils.dirac_delta(x, 1)
    return x, n
