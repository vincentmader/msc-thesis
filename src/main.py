#!/usr/bin/env python3
import numpy as np

from config import X_MIN, X_MAX, GRID_RESOLUTION


def initialize_state():
    x = np.linspace(X_MIN, X_MAX, GRID_RESOLUTION)
    n = np.array([1] + [0] * (GRID_RESOLUTION-1))
    return x, n


def main():
    x, n0 = initialize_state()


if __name__ == "__main__":
    main()
