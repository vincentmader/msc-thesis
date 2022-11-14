import numpy as np
from numba import jit

from utils.mass_index_conversion import mass_from_index, index_from_mass


@jit(nopython=True)
def K(
    mass_grid_resolution,
    mass_grid_exp_min,
    mass_grid_stepsize,
    coagulation_kernel_variant,
):
    K_gain = np.zeros((mass_grid_resolution, mass_grid_resolution, mass_grid_resolution))
    K_loss = np.zeros((mass_grid_resolution, mass_grid_resolution, mass_grid_resolution))

    for i in range(mass_grid_resolution):
        for j in range(mass_grid_resolution):
            # Determine masses before & after hit-and-stick collision.
            m_i = mass_from_index(i, mass_grid_exp_min, mass_grid_stepsize)
            m_j = mass_from_index(j, mass_grid_exp_min, mass_grid_stepsize)
            m = m_i + m_j

            # Determine index of bins adjacent to combined mass.
            k_l = index_from_mass(m, mass_grid_exp_min, mass_grid_stepsize)
            k_h = k_l + 1  # TODO handle cases where `k_h == mass_grid_resolution`

            # Get mass corresponding to these indices.
            m_l = mass_from_index(k_l, mass_grid_exp_min, mass_grid_stepsize)
            m_h = mass_from_index(k_h, mass_grid_exp_min, mass_grid_stepsize)

            # Calculate loss term (gain term can then be calculated from this).
            K_l = K_ij_loss(
                i,
                j,
                mass_grid_exp_min,
                mass_grid_stepsize,
                coagulation_kernel_variant,
            )

            # Use linear ansatz to split kernel between adjacent next-lower/-higher bins.
            eps = (m_i + m_j - m_l) / (m_h - m_l)

            # Add gain-term to adjacent "next-lower" bin.
            K_gain[k_l][i][j] += K_l * (1-eps)
            # Add gain-term to adjacent "next-higher" bin.
            K_gain[k_h][i][j] += K_l * eps
            # Add loss term.
            K_loss[i][i][j] -= K_l

    return K_gain, K_loss


@jit(nopython=True)
def K_ij_loss(
    i,
    j,
    mass_grid_exp_min,
    mass_grid_stepsize,
    coagulation_kernel_variant,
):
    if coagulation_kernel_variant == "constant":
        K_kij = 1

    elif coagulation_kernel_variant == "linear":
        m_i = mass_from_index(i, mass_grid_exp_min, mass_grid_stepsize)
        m_j = mass_from_index(j, mass_grid_exp_min, mass_grid_stepsize)
        K_kij = m_i + m_j

    elif coagulation_kernel_variant == "quadratic":
        m_i = mass_from_index(i, mass_grid_exp_min, mass_grid_stepsize)
        m_j = mass_from_index(j, mass_grid_exp_min, mass_grid_stepsize)
        K_kij = m_i * m_j

    else:
        raise Exception("Kernel variant is undefined.")

    return K_kij
