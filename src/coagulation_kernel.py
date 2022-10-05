from numba import jit


@jit(nopython=True)
def coagulation_kernel(x, y):
    return 1
