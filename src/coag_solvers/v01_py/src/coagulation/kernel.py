import numpy as np
from numba import jit

from config import GRID_EXP_MIN
from config import GRID_STEPSIZE
from config import GRID_RESOLUTION as GRID_RES
from config import KERNEL_VARIANT

# TODO Make sure that k_h <= GRID_RES at all times.
#      Where? -> At definition `k_h = k_l + 1`.
#             -> Prevent index-out-of-bounds error!


@jit(nopython=True)
def K(
    handle_near_zero_cancellation=True,
):
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

            # Calculate loss term.
            K_l = K_ij_loss(i, j)

            # Use linear ansatz to split kernel between adjacent next-lower/-higher bins.
            eps = (m_i + m_j - m_l) / (m_h - m_l)
            K_g_l = K_l * (1 - eps)
            K_g_h = K_l * eps

            if k_l == max(i, j):
                could_cancel = True
            elif k_l > max(i, j):
                could_cancel = False
            else:
                raise Exception("ERROR: This should never happen.")

            # Add gain-term to adjacent "next-lower" bin.
            K_gain[k_l][i][j] += K_g_l
            # Add gain-term to adjacent "next-higher" bin.
            K_gain[k_h][i][j] += K_g_h
            # Add loss term.
            K_loss[i][i][j] -= K_l

    return K_gain, K_loss


@jit(nopython=True)
def K_ij_loss(i, j):
    if KERNEL_VARIANT == "constant":
        K_kij = 1
    elif KERNEL_VARIANT == "linear":
        K_kij = mass_from_index(i) + mass_from_index(j)
    elif KERNEL_VARIANT == "quadratic":
        K_kij = mass_from_index(i) * mass_from_index(j)
    else:
        raise Exception(
            f"ERROR: Kernel variant \"{KERNEL_VARIANT}\" is not defined.")
    return K_kij


@jit(nopython=True)
def mass_from_index(idx):
    return (10**GRID_EXP_MIN) * (GRID_STEPSIZE**idx)


@jit(nopython=True)
def index_from_mass(mass):
    return int(
        (np.log(mass) - GRID_EXP_MIN*np.log(10)) /
        (np.log(GRID_STEPSIZE))
    )
