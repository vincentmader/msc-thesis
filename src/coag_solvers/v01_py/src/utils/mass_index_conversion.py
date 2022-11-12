import numpy as np
from numba import jit

from config import GRID_EXP_MIN
from config import GRID_STEPSIZE


@jit(nopython=True)
def mass_from_index(idx):
    return (10**GRID_EXP_MIN) * (GRID_STEPSIZE**idx)


@jit(nopython=True)
def index_from_mass(mass):
    res = (np.log(mass) - GRID_EXP_MIN*np.log(10)) / (np.log(GRID_STEPSIZE))
    return int(res)
