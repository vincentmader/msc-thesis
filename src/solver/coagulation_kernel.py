import numpy as np
from numba import jit
from utils import kronecker_delta

from config import GRID_EXP_MIN, GRID_STEPSIZE
from config import GRID_RESOLUTION as RES


@jit(nopython=True)
def create_coagulation_kernel():
    K = np.zeros((RES, RES, RES))

    # Determine loss contribution.
    for k in range(RES):
        for i in range(RES):
            for j in range(RES):
                K_l = K_ij_loss(i, j) * kronecker_delta(k, i)
                K[k][i][j] -= K_l

    # Determine gain contribution.
    for i in range(RES):
        for j in range(RES):
            m_i = mass_from_index(i)
            m_j = mass_from_index(j)
            m = m_i + m_j

            k_l = index_from_mass(m)
            k_h = k_l + 1

            m_l = mass_from_index(k_l)
            m_h = mass_from_index(k_h)

            K_l = K_ij_loss(i, j)
            eps = (m_i + m_j - m_l) / (m_h - m_l)
            K_g_l = K_l * (1 - eps)
            K_g_h = K_l * eps

            K[k_l][i][j] += 1/2 * K_g_l
            K[k_h][i][j] += 1/2 * K_g_h
    # Return total kernel.
    return K


@jit(nopython=True)
def K_kij_gain(k, i, j):
    return 1


@jit(nopython=True)
def K_ij_loss(i, j):
    return 1


@jit(nopython=True)
def mass_from_index(idx):
    return (10**GRID_EXP_MIN) * (GRID_STEPSIZE**idx)


@jit(nopython=True)
def index_from_mass(mass):
    return int(
        (np.log(mass) - GRID_EXP_MIN*np.log(10)) /
        (np.log(GRID_STEPSIZE))
    )
