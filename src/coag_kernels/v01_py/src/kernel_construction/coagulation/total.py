import numpy as np

from config import Config
from collision import collision_and_merge_rate as R
from utils.elementary_functions import heaviside_theta
from utils.mass_index_conversion import mass_from_index
from utils.mass_index_conversion import index_from_mass


def construct_total_kernel(cfg: Config):
    # Initialize kernel as 3D matrix of zeros.
    K = np.zeros(shape=[cfg.mass_grid_resolution]*3)

    # Initialize mass grid.
    indices = np.arange(0, K.shape[0], 1)
    masses = mass_from_index(indices, cfg)

    # Loop over all possible particle-particle pairs in the discrete mass grid.
    for i, m_i in zip(indices, masses):
        for j, m_j in zip(indices, masses):

            # Calculate mass after hit-and-stick collision.
            m_k = m_i + m_j
            # Determine indices of bins adjacent to combined mass.
            k_l = index_from_mass(m_k, cfg)
            k_h = k_l + 1

            # If indices of combined mass lie outside the mass grid: -> Skip.
            if max(k_l, k_h) >= cfg.mass_grid_resolution:
                continue
            # Calculate the mass corresponding to the two indices.
            m_l = mass_from_index(k_l, cfg)
            m_h = mass_from_index(k_h, cfg)

            # Calculate loss term (gain term can then be calculated from this).
            R_kij = R(i, j, cfg)

            # Determine prefactor of gain-term.
            f_gain = heaviside_theta(i - j)

            # Check whether cancellation-handling needs to be done.
            might_cancel = (k_l == i)
            trivial = not (cfg.handle_near_zero_cancellation and might_cancel)
            if trivial:
                eps = (m_i + m_j - m_l) / (m_h - m_l)
                K[i, i, j] -= R_kij
                K[k_l, i, j] += R_kij * f_gain * (1-eps)
                K[k_h, i, j] += R_kij * f_gain * eps
            else:
                eps = m_j / (m_h - m_l)  # NOTE 2nd case of cancellation
                K[k_l, i, j] -= R_kij * f_gain * eps
                if i == j:
                    K[k_l, i, j] -= 1/2 * R_kij   # NOTE no eps here
                K[k_h, i, j] += R_kij * f_gain * eps

    return K
