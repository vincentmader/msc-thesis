import numpy as np

import utils


def initial_state(cfg):
    x = np.logspace(cfg.mass_grid_exp_min, cfg.mass_grid_exp_max, cfg.mass_grid_resolution)

    if cfg.initial_mass_distribution == "gaussian":
        # mu, sigma = 10**(-5), 10**(-7)
        # n = utils.gaussian(x, mu, sigma)
        raise Exception("TODO implement Gaussian in log-representation")

    elif cfg.initial_mass_distribution == "dirac-delta":
        idx0 = 10
        n = utils.dirac_delta(x, idx0)

    else:
        raise Exception(
            f"ERROR: Initial state {cfg.initial_mass_distribution} is not defined.")
    return x, n
