import numpy as np

from config import Config
import utils


def get_initial_mass_distribution(cfg: Config, x):
    r"""Constructs initial particle mass distribution $N(m)=n(m)\cdot\Delta m$.

    Arguments:
    - cfg:  simulation configuration
    - x:    mass grid
    """
    variant = cfg.initial_mass_distribution

    if variant == "dirac-delta":
        idx0 = 2  # TODO
        return utils.dirac_delta(x, idx0)

    elif variant == "gaussian":
        mu = 1e-5  # TODO
        sigma = 1e-7  # TODO
        return utils.gaussian(x, mu, sigma)

    elif variant == "flat":
        return np.ones(x.shape[0]) / x.shape[0]

    elif variant == "flatter":
        return np.ones(x.shape[0]) / x.shape[0]

    else:
        raise Exception(f"Unknown mass distribution \"{variant}\".")
