import matplotlib.pyplot as plt
from numpy import float64 as f64

# Define Discretization of Time-Axis (Abscissa).
# -----------------------------------------------------------------------------

# Define number of forward-steps.
NR_OF_TIMESTEPS = 700

# Define Discretization of Mass-Axis (Ordinate).
# -----------------------------------------------------------------------------

# Define number of points in mass-grid.
GRID_RESOLUTION = 100

# Define minimum & maximum exponent of logarithmic mass-grid.
GRID_EXP_MIN = f64(-5)
GRID_EXP_MAX = f64(+5)

# Define (multiplicative) step-size from one mass-grid-point to the next.
GRID_STEPSIZE = (10**(GRID_EXP_MAX-GRID_EXP_MIN))**(1/GRID_RESOLUTION)

# Define the initial state.
# -----------------------------------------------------------------------------

# At the moment, this could be either
#   - "gaussian" or
#   - "dirac-delta".
INITIAL_STATE = "dirac-delta"

# Define paths to directories on disk.
# -----------------------------------------------------------------------------

# Define path to directory where simulation-data shall be saved.
PATH_TO_DATA = "./data"

# Define path to directory where figures shall be saved.
PATH_TO_FIGURES = "./figures"

# Configure plotting.
# -----------------------------------------------------------------------------

# Define nr. of time-steps between plotting.
STEPS_BETWEEN_PLOT = 100

# Define matplotlib theme & apply.
MPL_THEME = "~/.config/matplotlib/dark.mplstyle"
plt.style.use(MPL_THEME)

# Define plot size.
FIG_SIZE = (12, 8)

# Various (as of yet unused).
# -----------------------------------------------------------------------------

# Define plot variants.
# PLOT_VARIANTS   = [
#     "lin-x",
#     "log-x",
# ]
