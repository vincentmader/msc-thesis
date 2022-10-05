# Define discretization in time.
NR_OF_TIMESTEPS = 4
DT              = 1

# Define discretization in mass.
X_MIN, X_MAX    = 0, 10
GRID_RESOLUTION = 10

# Define initial state. 
# Options:
#  - "gaussian"
#  - "dirac-delta"
INITIAL_STATE   = "dirac-delta"  

# Define paths to figure & data directories.
PATH_TO_FIGURES = "./figures"
PATH_TO_DATA    = "./data"
