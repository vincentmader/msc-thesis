import kernel_construction.coagulation as coagulation
import kernel_construction.fragmentation as fragmentation


def kernel(cfg):
    K_coag = coagulation.kernel(cfg)
    K_frag = fragmentation.kernel(cfg)
    K = K_coag + K_frag
    return K
