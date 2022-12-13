import numpy as np


def mass_from_index(idx, cfg):
    variant = cfg.mass_grid_variant
    min_value = cfg.mass_grid_min_value
    stepsize = cfg.mass_grid_stepsize
    if variant == "logarithmic":
        return (10**min_value) * (stepsize**idx)
    else:
        return min_value + stepsize*idx


def index_from_mass(mass, cfg):
    variant = cfg.mass_grid_variant
    min_value = cfg.mass_grid_min_value
    stepsize = cfg.mass_grid_stepsize

    if variant == "logarithmic":
        res = (np.log(mass) - min_value*np.log(10)) / np.log(stepsize)
        return int(res)
    else:
        res = (mass - min_value) / stepsize
        return int(res)
