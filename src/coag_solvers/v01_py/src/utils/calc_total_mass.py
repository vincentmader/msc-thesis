import numpy as np
from utils.mass_index_conversion import mass_from_index


def calc_total_mass(n, mass_grid_exp_min, mass_grid_stepsize):
    # m_i = lambda i: mass_from_index(i, mass_grid_exp_min, mass_grid_stepsize)
    def m_i(i): return mass_from_index(
        i, mass_grid_exp_min, mass_grid_stepsize)

    indices = np.arange(0, len(n), 1)
    m_tot = sum(m_i(indices) * n)
    # m_tot = sum([m_i(i) * n_i for i, n_i in enumerate(n)])
    return m_tot
