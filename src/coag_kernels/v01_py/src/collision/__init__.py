from utils.mass_index_conversion import mass_from_index


def collision_and_merge_rate(i, j, cfg):
    m_i = mass_from_index(i, cfg)
    m_j = mass_from_index(j, cfg)

    if cfg.coagulation_kernel_variant == "constant":
        res = 1

    elif cfg.coagulation_kernel_variant == "linear":
        res = m_i + m_j

    elif cfg.coagulation_kernel_variant == "quadratic":
        res = m_i * m_j

    else:
        raise Exception("Kernel variant is undefined.")

    return res
