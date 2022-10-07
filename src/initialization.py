import numpy as np

from config import INITIAL_STATE, X
import utils


def get_initial_state():
    if INITIAL_STATE == "gaussian":
        mu, sigma = 5, 2
        n = utils.gaussian(X, mu, sigma)

    elif INITIAL_STATE == "dirac-delta":
        x0 = 1
        n = utils.dirac_delta(X, x0)

    else:
        raise Exception(
            f"ERROR: Initial state {INITIAL_STATE} is not defined.")
    return n
