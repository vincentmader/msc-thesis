import numpy as np
from numba import njit

from utils.mass_index_conversion import mass_from_index, index_from_mass
from utils.elementary_functions import heaviside_theta


def K(cfg):
    mass_grid_resolution = cfg.mass_grid_resolution
    mass_grid_exp_min = cfg.mass_grid_exp_min
    mass_grid_stepsize = cfg.mass_grid_stepsize

    K = np.zeros(shape=(mass_grid_resolution, mass_grid_resolution, mass_grid_resolution))

    for i in range(K.shape[1]):
        m_i = mass_from_index(i, mass_grid_exp_min, mass_grid_stepsize)
        for j in range(K.shape[2]):
            m_j = mass_from_index(j, mass_grid_exp_min, mass_grid_stepsize)

            # Determine masses before & after hit-and-stick collision.
            m_k = m_i + m_j

            # Determine indices of bins adjacent to combined mass.
            k_l = index_from_mass(m_k, mass_grid_exp_min, mass_grid_stepsize)
            k_h = k_l + 1

            # Check if indices of resulting mass(es) lie outside the discrete mass grid.
            if k_l >= mass_grid_resolution or k_h >= mass_grid_resolution:
                # print("i =", i, ", j =", j, "-> k_l =", k_l)
                # print("                -> k_h =", k_h, "\n")
                continue

            # Get mass corresponding to these indices.
            m_l = mass_from_index(k_l, mass_grid_exp_min, mass_grid_stepsize)
            m_h = mass_from_index(k_h, mass_grid_exp_min, mass_grid_stepsize)

            # Calculate loss term (gain term can then be calculated from this).
            R_kij = R(i, j, cfg)

            # Use linear ansatz to split kernel between adjacent next-lower/-higher bins.
            eps = (m_i + m_j - m_l) / (m_h - m_l)

            # Determine prefactor of gain-term.
            r_gain = heaviside_theta(i - j)

            if not cfg.handle_near_zero_cancellation:
                # Add gain-term to adjacent "next-higher" bin.
                K[k_h][i][j] += r_gain * R_kij * eps
                # Add gain-term to adjacent "next-lower" bin.
                K[k_l][i][j] += r_gain * R_kij * (1-eps)
                # Add loss term.
                K[i][i][j] -= R_kij

            else:
                if k_l > max(i, j):
                    K[k_h][i][j] += r_gain * R_kij * eps
                    K[k_l][i][j] += r_gain * R_kij * (1-eps)
                    K[i][i][j] -= R_kij

                elif k_l == i:
                    pass

                elif k_l == j:
                    pass

                else:
                    raise Exception

    if cfg.run_stability_tests:
        test_for_mass_conservation(cfg, K)

    return K


def R(i, j, cfg):
    mass_grid_exp_min = cfg.mass_grid_exp_min
    mass_grid_stepsize = cfg.mass_grid_stepsize
    coagulation_kernel_variant = cfg.coagulation_kernel_variant

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


def test_for_mass_conservation(cfg, K):
    mass_grid_resolution = cfg.mass_grid_resolution
    mass_grid_exp_min = cfg.mass_grid_exp_min
    mass_grid_stepsize = cfg.mass_grid_stepsize

    good, bad, skipped, total = 0, 0, 0, 0
    for i in range(mass_grid_resolution):
        m_i = mass_from_index(i, mass_grid_exp_min, mass_grid_stepsize)
        for j in range(mass_grid_resolution):
            m_j = mass_from_index(j, mass_grid_exp_min, mass_grid_stepsize)
            m_k = m_i + m_j
            k_l = index_from_mass(m_k, mass_grid_exp_min, mass_grid_stepsize)
            k_h = k_l + 1
            if k_l >= mass_grid_resolution or k_h >= mass_grid_resolution:
                # print("i =", i, ", j =", j, "-> k_l =", k_l)
                # print("                -> k_h =", k_h, "\n")
                skipped += 1
                continue
            m_l = mass_from_index(k_l, mass_grid_exp_min, mass_grid_stepsize)
            m_h = mass_from_index(k_h, mass_grid_exp_min, mass_grid_stepsize)

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
