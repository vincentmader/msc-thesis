import numpy as np
from numba import jit

from config import GRID_RESOLUTION as GRID_RES
from config import COAGULATION_KERNEL_VARIANT
from utils.mass_index_conversion import mass_from_index, index_from_mass

# TODO Make sure that k_h <= GRID_RES at all times.
#      Where? -> At definition `k_h = k_l + 1`.
#             -> Prevent index-out-of-bounds error!


@jit(nopython=True)
def K():
    K_gain = np.zeros((GRID_RES, GRID_RES, GRID_RES))
    K_loss = np.zeros((GRID_RES, GRID_RES, GRID_RES))

    for i in range(GRID_RES):
        for j in range(GRID_RES):
            # Determine masses before & after hit-and-stick collision.
            m_i = mass_from_index(i)
            m_j = mass_from_index(j)
            m = m_i + m_j

            # Determine index of bins adjacent to combined mass.
            k_l = index_from_mass(m)
            k_h = k_l + 1

            # Get mass corresponding to these indices.
            m_l = mass_from_index(k_l)
            m_h = mass_from_index(k_h)

            # Calculate loss term (gain term can then be calculated from this).
            K_l = K_ij_loss(i, j)

            # Use linear ansatz to split kernel between adjacent next-lower/-higher bins.
            eps = (m_i + m_j - m_l) / (m_h - m_l)

            # Add gain-term to adjacent "next-lower" bin.
            K_gain[k_l][i][j] += K_l * (1-eps)
            # Add gain-term to adjacent "next-higher" bin.
            K_gain[k_h][i][j] += K_l * eps
            # Add loss term.
            K_loss[i][i][j] -= K_l

    # i = 0
    # j = 1
    # m_i = mass_from_index(i)
    # m_j = mass_from_index(j)
    # print("m_i =", m_i)
    # print("m_j =", m_j)

    # m = m_i + m_j
    # k_l = index_from_mass(m)
    # k_h = k_l + 1
    # print("k_l =", k_l)
    # print("k_h =", k_h)

    # m_l = mass_from_index(k_l)
    # m_h = mass_from_index(k_h)

    # eps = (m_i + m_j - m_l) / (m_h - m_l)
    # print("eps =", eps)

    # a = m_i * K_gain[k_l][i][j] + m_j * K_gain[k_h][i][j]
    # b = (m_i + m_j) *  K_loss[i][i][j]
    # if a != b:
    #     print()
    #     print(a)
    #     print(b)
    #     if b == -2*a:
    #         print("1/2")

    return K_gain, K_loss


@jit(nopython=True)
def K_ij_loss(i, j):
    if COAGULATION_KERNEL_VARIANT == "constant":
        K_kij = 1
    elif COAGULATION_KERNEL_VARIANT == "linear":
        K_kij = mass_from_index(i) + mass_from_index(j)
    elif COAGULATION_KERNEL_VARIANT == "quadratic":
        K_kij = mass_from_index(i) * mass_from_index(j)
    else:
        raise Exception(
            f"ERROR: Kernel variant \"{COAGULATION_KERNEL_VARIANT}\" is not defined.")
    return K_kij
