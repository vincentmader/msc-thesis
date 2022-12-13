import numpy as np
from utils.mass_index_conversion import mass_from_index


def calc_total_mass(n, cfg):
    m_i = lambda i: mass_from_index(i, cfg)
    indices = np.arange(0, len(n), 1)
    m_tot = sum(m_i(indices) * n)
    return m_tot
