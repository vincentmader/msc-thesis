from kernel_construction.coagulation.total import construct_total_kernel
from kernel_construction.coagulation.gain import construct_gain_term
from kernel_construction.coagulation.loss import construct_loss_term


def kernel(cfg):
    if cfg.handle_near_zero_cancellation:
        K = construct_total_kernel(cfg)
    else:
        K_gain = construct_gain_term(cfg)
        K_loss = construct_loss_term(cfg)
        K = K_gain + K_loss

    return K


# def test_for_mass_conservation(cfg, K):
#     good, bad, skipped, total = 0, 0, 0, 0
#     for i in range(K.shape[0]):
#         m_i = mass_from_index(i, cfg)
#         for j in range(K.shape[1]):
#             m_j = mass_from_index(j, cfg)
#             m_k = m_i + m_j
#             k_l = index_from_mass(m_k, cfg)
#             k_h = k_l + 1
#             if max(k_l, k_h) >= cfg.mass_grid_resolution:
#                 # print("i =", i, ", j =", j, "-> k_l =", k_l)
#                 # print("                -> k_h =", k_h, "\n")
#                 skipped += 1
#                 continue
#             m_l = mass_from_index(k_l, cfg)
#             m_h = mass_from_index(k_h, cfg)

#             a = m_l * K[k_l][i][j] + m_h * K[k_h][i][j]
#             b = (m_i + m_j) * K[i][i][j]
#             if a != b:
#                 if (a-b)/b > 10e-16:
#                     bad += 1
#                 else:
#                     good += 1
#             else:
#                 good += 1

#     total = good + bad + skipped
#     print("\tChecking mass conservation (eq. 1.21) up to 10^-16")
#     print("\tgood:    ", good, "\t/", total)
#     print("\tbad:     ", bad, "\t/", total)
#     print("\tskipped: ", skipped, "\t/", total)
#     print("\n\t-> Accuracy:", round(good/(bad+good)*100), "% (for non-skipped)")
