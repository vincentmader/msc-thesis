import numpy as np

# Define Discretization of Time-Axis (Abscissa).
# -----------------------------------------------------------------------------

# Define number of forward-steps.
NR_OF_TIMESTEPS = 4

# Define size of a single time-step.
DT              = 1

# Define Discretization of Mass-Axis (Ordinate).
# -----------------------------------------------------------------------------

# Define minumum & maximum x-value.
X_MIN           = 0
X_MAX           = 100

# Define number of points in mass-grid.
GRID_RESOLUTION = 100

# Use the above to define the mass-axis.
X               = np.linspace(X_MIN, X_MAX, GRID_RESOLUTION)

# Define the initial state.
# -----------------------------------------------------------------------------

# At the moment, this could be either
#   - "gaussian" or 
#   - "dirac-delta".
INITIAL_STATE   = "gaussian"  

# Define path to directories on disk.
# -----------------------------------------------------------------------------

# Define path to directory where simulation-data shall be saved.
PATH_TO_DATA    = "./data"

# Define path to directory where figures shall be saved.
PATH_TO_FIGURES = "./figures"

# Configure plotting.
# -----------------------------------------------------------------------------

# Define matplotlib theme.
MPL_THEME       = "~/.config/matplotlib/dark.mplstyle"

# Define plot size.
FIG_SIZE        = (12, 8)

# Various (as of yet unused).
# -----------------------------------------------------------------------------

# Define plot variants.
# PLOT_VARIANTS   = [
#     "lin-x", 
#     "log-x",
# ]
