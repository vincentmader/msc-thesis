from config import Config
import kernel_construction.coagulation as coagulation
import kernel_construction.fragmentation as fragmentation


def kernel(cfg: Config):
    """Constructs kernel for use in integration of Smoluchowski equations.

    Arguments:
    - cfg:  simulation configuration

    Returns:
    - K:    3D matrix consisting of both coagulation & fragmentation terms.
    """

    K_coag = coagulation.kernel(cfg)
    K_frag = fragmentation.kernel(cfg)

    K = K_coag + K_frag

    return K
