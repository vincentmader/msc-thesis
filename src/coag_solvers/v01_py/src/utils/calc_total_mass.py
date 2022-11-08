def calc_total_mass(x, n):
    m_tot = sum(x_i * n_i for x_i, n_i in zip(x, n))
    return m_tot
