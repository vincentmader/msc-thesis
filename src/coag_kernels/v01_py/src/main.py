import sys

import numpy as np

from config import Config
import utils
from utils import mass_index_conversion
from utils.elementary_functions import heaviside_theta

def save_kernel_to_file():
    pass


def K(cfg):
    # Define short-hand notation for index-to-mass conversion.
    mass_from_index = lambda idx: mass_index_conversion.mass_from_index(
        idx, cfg.mass_grid_exp_min, cfg.mass_grid_stepsize
    )
    # Define short-hand notation for mass-to-index conversion.
    index_from_mass = lambda mass: mass_index_conversion.index_from_mass(
        mass, cfg.mass_grid_exp_min, cfg.mass_grid_stepsize
    )

    # Initialize kernel as 3D matrix of zeros.
    K = np.zeros(shape=[cfg.mass_grid_resolution]*3)
    # Loop over all possible particle-particle pairs in the discrete mass grid.
    for i in range(K.shape[0]):
        m_i = mass_from_index(i)
        for j in range(K.shape[1]):
            m_j = mass_from_index(j)

            # Determine masses before & after hit-and-stick collision.
            m_k = m_i + m_j
            # Determine indices of bins adjacent to combined mass.
            k_l = index_from_mass(m_k)
            k_h = k_l + 1
            # Check if indices of resulting mass(es) lie 
            # outside the discrete mass grid. If yes: -> Skip.
            if max(k_l, k_h) >= cfg.mass_grid_resolution:
                continue

            # Calculate the mass corresponding to these indices.
            m_l = mass_from_index(k_l)
            m_h = mass_from_index(k_h)
            # Calculate loss term (gain term can then be calculated from this).
            R_kij = R(i, j, cfg, mass_from_index)
            # Use linear ansatz to split kernel between adjacent next-lower/-higher bins.
            eps = (m_i + m_j - m_l) / (m_h - m_l)
            # Determine prefactor of gain-term.
            f_gain = heaviside_theta(i - j)

            might_cancel = k_l == i
            trivial = not (cfg.handle_near_zero_cancellation and might_cancel)
            if trivial:
                K[  i, i, j] -= R_kij
                K[k_l, i, j] += R_kij * f_gain * (1-eps)
                K[k_h, i, j] += R_kij * f_gain * eps
            else:
                K[k_l, i, j] -= R_kij * f_gain * eps
                K[k_h, i, j] += R_kij * f_gain * eps
    
    if cfg.run_stability_tests:
        test_for_mass_conservation(cfg, K, mass_from_index, index_from_mass)

    return K


def R(i, j, cfg, mass_from_index):
    coagulation_kernel_variant = cfg.coagulation_kernel_variant

    m_i = mass_from_index(i)
    m_j = mass_from_index(j)

    if coagulation_kernel_variant == "constant":
        res = 1

    elif coagulation_kernel_variant == "linear":
        res = m_i + m_j

    elif coagulation_kernel_variant == "quadratic":
        res = m_i * m_j

    else:
        raise Exception("Kernel variant is undefined.")

    return res


def test_for_mass_conservation(cfg, K, mass_from_index, index_from_mass):
    good, bad, skipped, total = 0, 0, 0, 0
    for i in range(K.shape[0]):
        m_i = mass_from_index(i)
        for j in range(K.shape[1]):
            m_j = mass_from_index(j)
            m_k = m_i + m_j
            k_l = index_from_mass(m_k)
            k_h = k_l + 1
            if max(k_l,k_h) >= cfg.mass_grid_resolution:
                # print("i =", i, ", j =", j, "-> k_l =", k_l)
                # print("                -> k_h =", k_h, "\n")
                skipped += 1
                continue
            m_l = mass_from_index(k_l)
            m_h = mass_from_index(k_h)

            a = m_l * K[k_l][i][j] + m_h * K[k_h][i][j]
            b = (m_i + m_j) * K[i][i][j]
            if a != b:
                if (a-b)/b > 10e-16:
                    bad += 1
                else:
                    good += 1
            else:
                good += 1

    total = good + bad + skipped
    print("\tChecking mass conservation (eq. 1.21) up to 10^-16")
    print("\tgood:    ", good, "\t/", total)
    print("\tbad:     ", bad, "\t/", total)
    print("\tskipped: ", skipped, "\t/", total)
    print("\n\t-> Accuracy:", round(good/(bad+good)*100), "% (for non-skipped)")


if __name__ == "__main__":
    # Load solver configuration from TOML file.
    cfg = Config()

    kernel = K(cfg)

    run_id = sys.argv[1]

    # Save kernel(s) to file.
    utils.file_io.save_coagulation_kernel_to_file(cfg, run_id, kernel)
