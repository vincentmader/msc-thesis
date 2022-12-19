import numpy as np

from config import Config


def get_mass_grid(cfg: Config):
    variant = cfg.mass_grid_variant
    resolution = cfg.mass_grid_resolution

    if variant == "logarithmic":
        e_min = cfg.mass_grid_min_value
        e_max = cfg.mass_grid_max_value
        return np.logspace(e_min, e_max, resolution)

    elif variant == "linear":
        m_min = cfg.mass_grid_min_value
        m_max = cfg.mass_grid_max_value
        return np.linspace(m_min, m_max, resolution)

    else:
        msg = f"Unknown mass grid \"{variant}\"."
        raise Exception(msg)
