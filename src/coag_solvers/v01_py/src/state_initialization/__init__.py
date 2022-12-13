import numpy as np

import utils


def initial_state(cfg):
    if cfg.mass_grid_variant == "logarithmic":
        exp_min = cfg.mass_grid_min_value
        exp_max = cfg.mass_grid_max_value
        N_m = cfg.mass_grid_resolution
        x = np.logspace(exp_min, exp_max, N_m)
    else:
        m_min = cfg.mass_grid_min_value
        m_max = cfg.mass_grid_max_value
        N_m = cfg.mass_grid_resolution
        x = np.linspace(m_min, m_max, N_m)

    if cfg.initial_mass_distribution == "gaussian":
        # mu, sigma = 10**(-5), 10**(-7)
        # n = utils.gaussian(x, mu, sigma)
        raise Exception("TODO implement Gaussian in log-representation")

    elif cfg.initial_mass_distribution == "dirac-delta":
        idx0 = 2
        n = utils.dirac_delta(x, idx0)

    elif cfg.initial_mass_distribution == "flat":
        n = np.ones(x.shape[0]) / x.shape[0]

    else:
        raise Exception(
            f"ERROR: Initial state {cfg.initial_mass_distribution} is not defined.")

    return x, n
