import numpy as np
from numba import jit
from utils import kronecker_delta

from config import GRID_RESOLUTION as RES
import utils


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
            # assert m_l == m_i+m_j

            K_l = K_ij_loss(i, j)  # * kronecker_delta(k, i)
            eps = (m_i + m_j - m_l) / (m_h - m_l)
            K_g_l = K_l * (1 - eps)
            K_g_h = K_l * eps
            # assert (K_g_l, K_g_h) == (1, 0)

            K[k_l][i][j] += 1/2 * K_g_l
            K[k_h][i][j] += 1/2 * K_g_h
    # Return total kernel.
    return K


def create_coagulation_kernel_2():
    K = np.zeros(shape=(RES, RES, RES))
    for k in range(RES):
        for i in range(RES):
            for j in range(RES):
                K[k][i][j] += K_kij(k, i, j)
    return K


@jit(nopython=True)
def K_kij(k, i, j):
    K_l = K_ij_loss(i, j) * utils.kronecker_delta(k, i)
    K_g = K_kij_gain(k, i, j) * utils.kronecker_delta(k, i+j)
    return K_g/2 - K_l


@jit(nopython=True)
def K_kij_gain(k, i, j):
    return 1


@jit(nopython=True)
def K_ij_loss(i, j):
    return 1


@jit(nopython=True)
def mass_from_index(idx):
    # TODO adjust for log-grid
    return idx


@jit(nopython=True)
def index_from_mass(mass):
    # TODO determine index from mass value
    return mass
