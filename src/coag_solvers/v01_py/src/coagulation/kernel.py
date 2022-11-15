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
    res = np.zeros(shape=(mass_grid_resolution, mass_grid_resolution, mass_grid_resolution))
    for i in range(mass_grid_resolution):
        m_i = mass_from_index(i, mass_grid_exp_min, mass_grid_stepsize)
        for j in range(mass_grid_resolution):
            m_j = mass_from_index(j, mass_grid_exp_min, mass_grid_stepsize)

            # Determine masses before & after hit-and-stick collision.
            m_k = m_i + m_j
            # Determine index of bins adjacent to combined mass.
            k_l = index_from_mass(m_k, mass_grid_exp_min, mass_grid_stepsize)
            k_h = k_l + 1  
            # Get mass corresponding to these indices.
            m_l = mass_from_index(k_l, mass_grid_exp_min, mass_grid_stepsize)
            m_h = mass_from_index(k_h, mass_grid_exp_min, mass_grid_stepsize)

            # Calculate loss term (gain term can then be calculated from this).
            K_l = R(i, j, mass_grid_exp_min, mass_grid_stepsize, coagulation_kernel_variant)

            # Use linear ansatz to split kernel between adjacent next-lower/-higher bins.
            eps = (m_i + m_j - m_l) / (m_h - m_l)

            if k_l == mass_grid_resolution or k_h == mass_grid_resolution:
                continue  # TODO handle cases where `k_h == mass_grid_resolution`

            # Add gain-term to adjacent "next-lower" bin.
            res[k_l][i][j] += 1/2 * K_l * (1-eps)
            # Add gain-term to adjacent "next-higher" bin.
            res[k_h][i][j] += 1/2 * K_l * eps
            # Add loss term.
            res[i][i][j] -= K_l

    return res


@jit(nopython=True)
def R(
    i,
    j,
    mass_grid_exp_min,
    mass_grid_stepsize,
    coagulation_kernel_variant,
):
    m_i = mass_from_index(i, mass_grid_exp_min, mass_grid_stepsize)
    m_j = mass_from_index(j, mass_grid_exp_min, mass_grid_stepsize)

    if coagulation_kernel_variant == "constant":
        res = 1

    elif coagulation_kernel_variant == "linear":
        res = m_i + m_j

    elif coagulation_kernel_variant == "quadratic":
        res = m_i * m_j

    else:
        raise Exception("Kernel variant is undefined.")

    return res
