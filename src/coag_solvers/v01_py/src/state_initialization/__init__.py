import numpy as np

import utils


def get_mass_grid(cfg):
    if cfg.mass_grid_variant == "logarithmic":
        exp_min = cfg.mass_grid_min_value
        exp_max = cfg.mass_grid_max_value
        x = np.logspace(exp_min, exp_max, cfg.mass_grid_resolution)
    else:
        m_min = cfg.mass_grid_min_value
        m_max = cfg.mass_grid_max_value
        x = np.linspace(m_min, m_max, cfg.mass_grid_resolution)
    return x

def get_initial_mass_distribution(cfg, x):
    if cfg.initial_mass_distribution == "dirac-delta":
        idx0 = 2
        N = utils.dirac_delta(x, idx0)

    elif cfg.initial_mass_distribution == "flat":
        N = np.ones(x.shape[0]) / x.shape[0]

    elif cfg.initial_mass_distribution == "true_flat":
        N = np.ones(x.shape[0]) / x.shape[0]

    elif cfg.initial_mass_distribution == "gaussian":
        mu, sigma = 10**(-5), 10**(-7)
        N = utils.gaussian(x, mu, sigma)
        raise Exception("TODO implement Gaussian in log-representation")

    else:
        raise Exception(
            f"ERROR: Initial state {cfg.initial_mass_distribution} is not defined.")
    return N


def get_initial_state(cfg):
    x = get_mass_grid(cfg)
    N = get_initial_mass_distribution(cfg, x)
    return x, N
