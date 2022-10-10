import numpy as np

from config import INITIAL_STATE
# from config import X_MIN, X_MAX
from config import GRID_EXP_MIN, GRID_EXP_MAX, GRID_RESOLUTION
import utils


def initial_state():
    x = np.logspace(GRID_EXP_MIN, GRID_EXP_MAX, GRID_RESOLUTION)

    if INITIAL_STATE == "gaussian":
        # TODO how to appropriately do in log-representation
        raise Exception("TODO implement Gaussian in log-representation")
        mu, sigma = 5, 2
        n = utils.gaussian(x, mu, sigma)

    elif INITIAL_STATE == "dirac-delta":
        idx0 = 10
        n = utils.dirac_delta(x, idx0)

    else:
        raise Exception(
            f"ERROR: Initial state {INITIAL_STATE} is not defined.")
    return x, n
