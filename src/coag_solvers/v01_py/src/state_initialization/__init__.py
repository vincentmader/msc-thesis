import numpy as np

from config import GRID_EXP_MIN, GRID_EXP_MAX, GRID_RESOLUTION
from config import INITIAL_STATE
import utils


def initial_state():
    x = np.logspace(GRID_EXP_MIN, GRID_EXP_MAX, GRID_RESOLUTION)

    if INITIAL_STATE == "gaussian":
        # mu, sigma = 10**(-5), 10**(-7)
        # n = utils.gaussian(x, mu, sigma)
        raise Exception("TODO implement Gaussian in log-representation")

    elif INITIAL_STATE == "dirac-delta":
        idx0 = 10
        n = utils.dirac_delta(x, idx0)

    else:
        raise Exception(
            f"ERROR: Initial state {INITIAL_STATE} is not defined.")
    return x, n
