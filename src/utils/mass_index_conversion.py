import numpy as np


def mass_from_index(idx, cfg):
    mass_grid_exp_min = cfg.mass_grid_exp_min
    mass_grid_stepsize = cfg.mass_grid_stepsize

    return (10**mass_grid_exp_min) * (mass_grid_stepsize**idx)


def index_from_mass(mass, cfg):
    mass_grid_exp_min = cfg.mass_grid_exp_min
    mass_grid_stepsize = cfg.mass_grid_stepsize

    res = (np.log(mass) - mass_grid_exp_min*np.log(10)) / (np.log(mass_grid_stepsize))
    return int(res)
