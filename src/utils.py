from datetime import datetime as dt

import numpy as np
from numba import float64 as f64


def gaussian(x, mu, sigma):
    y = np.exp(-((x-mu)/sigma)**2) / ((2*np.pi)**.5 * sigma)
    return y


def dirac_delta(x, i_x0):
    y = np.zeros(len(x))
    y[i_x0] = 1
    return y


def record_execution_time(f):
    start = dt.now()
    res = f()
    end = dt.now()
    duration = (end - start)
    return duration, res
