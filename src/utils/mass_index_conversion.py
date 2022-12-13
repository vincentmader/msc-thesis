import numpy as np


def mass_from_index(idx, cfg):
    mass_grid_stepsize = cfg.mass_grid_stepsize
    mass_grid_min = cfg.mass_grid_min
    if cfg.mass_grid_variant == "linear":
        raise Exception()
    elif cfg.mass_grid_variant == "logarithmic":
        return mass_grid_min * (mass_grid_stepsize**idx)
    else:
        raise Exception()


def index_from_mass(mass, cfg):
    mass_grid_min = cfg.mass_grid_min
    mass_grid_stepsize = cfg.mass_grid_stepsize
    if cfg.mass_grid_variant == "linear":
        raise Exception()
    elif cfg.mass_grid_variant == "logarithmic":
        print(mass, mass_grid_min)
        res = (np.log(mass) - mass_grid_min) / (np.log(mass_grid_stepsize))
        return int(res)
    else:
        raise Exception()
