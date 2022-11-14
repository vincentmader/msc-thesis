import numpy as np
from numba import jit


@jit(nopython=True)
def mass_from_index(idx, mass_grid_exp_min, mass_grid_stepsize):
    return (10**mass_grid_exp_min) * (mass_grid_stepsize**idx)


@jit(nopython=True)
def index_from_mass(mass, mass_grid_exp_min, mass_grid_stepsize):
    res = (np.log(mass) - mass_grid_exp_min*np.log(10)) / (np.log(mass_grid_stepsize))
    return int(res)
