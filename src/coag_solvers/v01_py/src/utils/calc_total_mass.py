from utils.mass_index_conversion import mass_from_index

def calc_total_mass(x, n, mass_grid_exp_min, mass_grid_stepsize):
    m_tot = sum(
        mass_from_index(i, mass_grid_exp_min, mass_grid_stepsize) * n_i for i, n_i in enumerate(n)
    )
    # m_tot = sum(x_i * n_i for x_i, n_i in zip(x, n))
    return m_tot
