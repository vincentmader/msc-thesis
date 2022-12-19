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
