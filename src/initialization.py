import numpy as np

from config import INITIAL_STATE
from config import X_MIN, X_MAX, GRID_RESOLUTION
import utils


def get_initial_state():
    x = np.linspace(X_MIN, X_MAX, GRID_RESOLUTION)

    if INITIAL_STATE == "gaussian":
        mu, sigma = 5, 2
        n = utils.gaussian(x, mu, sigma)

    elif INITIAL_STATE == "dirac-delta":
        x0 = 1
        n = utils.dirac_delta(x, x0)

    else:
        raise Exception(
            f"ERROR: Initial state {INITIAL_STATE} is not defined.")
    return x, n
