from state_initialization.mass_grid import get_mass_grid
from state_initialization.particle_mass_distribution import get_initial_mass_distribution


def get_initial_state(cfg):
    x = get_mass_grid(cfg)
    N = get_initial_mass_distribution(cfg, x)

    return x, N
