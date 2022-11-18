import numpy as np
from numba import jit

from utils.mass_index_conversion import mass_from_index, index_from_mass


@jit(nopython=True)
def K(
    mass_grid_resolution,
    mass_grid_exp_min,
    mass_grid_stepsize,
    coagulation_kernel_variant,
    run_stability_tests,
):
    K_gain = np.zeros(shape=(mass_grid_resolution, mass_grid_resolution, mass_grid_resolution))
    K_loss = np.zeros(shape=(mass_grid_resolution, mass_grid_resolution, mass_grid_resolution))

    for i in range(mass_grid_resolution):
        m_i = mass_from_index(i, mass_grid_exp_min, mass_grid_stepsize)
        for j in range(mass_grid_resolution):
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
            R_kij = R(i, j, mass_grid_exp_min, mass_grid_stepsize, coagulation_kernel_variant)

            # Use linear ansatz to split kernel between adjacent next-lower/-higher bins.
            eps = (m_i + m_j - m_l) / (m_h - m_l)

            # Add gain-term to adjacent "next-lower" bin.
            K_gain[k_l][i][j] += R_kij * (1-eps)

            # Add gain-term to adjacent "next-higher" bin.
            K_gain[k_h][i][j] += R_kij * eps

            # Add loss term.
            K_loss[i][i][j] += R_kij

    if run_stability_tests:
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

                a = m_l * K_gain[k_l][i][j] + m_h * K_gain[k_h][i][j]
                b = (m_i + m_j) * K_loss[i][i][j]
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

    return K_gain, K_loss


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
