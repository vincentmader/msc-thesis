import numpy as np

from config import Config
import utils


def get_initial_mass_distribution(cfg: Config, m):
    r"""Constructs initial particle mass distribution $N(m)=n(m)\cdot\Delta m$.

    Arguments:
    - cfg:  simulation configuration
    - m:    mass grid
    """
    variant = cfg.initial_mass_distribution
    resolution = cfg.mass_grid_resolution
    assert resolution == m.shape[0]

    if variant == "dirac-delta":
        idx0 = 2  # TODO
        return utils.dirac_delta(m, idx0)

    elif variant == "gaussian":
        mu = 1e-5  # TODO
        sigma = 1e-7  # TODO
        return utils.gaussian(m, mu, sigma)

    elif variant == "flat":
        return np.ones(resolution) / cfg.mass_grid_resolution

    elif variant == "flatter":
        if cfg.mass_grid_variant == "linear":
            raise Exception()
        elif cfg.mass_grid_variant == "logarithmic":
            C = 1 / (np.sum(1 / m))
            return C / m

    else:
        raise Exception(f"Unknown mass distribution \"{variant}\".")
