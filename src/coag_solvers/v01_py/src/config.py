from numpy import float64 as f64
import toml


CONFIG = toml.load("./config.toml")

# ╭───────────────────────────────────────────────────────────────────────────╮
# │ Solver                                                                    │
# ╰───────────────────────────────────────────────────────────────────────────╯

# Trivial: -> Python (v01)

# ╭───────────────────────────────────────────────────────────────────────────╮
# │ Mass Grid                                                                 │
# ╰───────────────────────────────────────────────────────────────────────────╯

# Define number of points in mass-grid.
GRID_RESOLUTION = CONFIG["mass_grid"]["mass_grid_resolution"]

# Define minimum & maximum exponent of logarithmic mass-grid.
GRID_EXP_MIN = f64(CONFIG["mass_grid"]["mass_exponent_min"])
GRID_EXP_MAX = f64(CONFIG["mass_grid"]["mass_exponent_max"])

# Define (multiplicative) step-size from one mass-grid-point to the next.
GRID_STEPSIZE = (10**(GRID_EXP_MAX-GRID_EXP_MIN))**(1/GRID_RESOLUTION)

# ╭───────────────────────────────────────────────────────────────────────────╮
# │ Initialization                                                            │
# ╰───────────────────────────────────────────────────────────────────────────╯

KERNEL_VARIANT = CONFIG["kernel"]["variant"]

# ╭───────────────────────────────────────────────────────────────────────────╮
# │ Initialization                                                            │
# ╰───────────────────────────────────────────────────────────────────────────╯

# Define the initial state.
INITIAL_STATE = CONFIG["initialization"]["initial_mass_distribution"]

# ╭───────────────────────────────────────────────────────────────────────────╮
# │ Simulation                                                                │
# ╰───────────────────────────────────────────────────────────────────────────╯

# Define Discretization of Time-Axis (Abscissa).
NR_OF_TIMESTEPS = CONFIG["simulation"]["nr_of_timesteps"]

# ╭───────────────────────────────────────────────────────────────────────────╮
# │ File-IO                                                                   │
# ╰───────────────────────────────────────────────────────────────────────────╯

# Define path to directory where figures shall be saved.
PATH_TO_CONFIG = CONFIG["file_io"]["path_to_config"]

PATH_TO_OUTFILES = CONFIG["file_io"]["path_to_outfiles"]

# Define path to directory where simulation-data shall be saved.
# PATH_TO_DATA = CONFIG["file_io"]["path_to_data"]

# Define path to directory where figures shall be saved.
# PATH_TO_FIGURES = CONFIG["file_io"]["path_to_figures"]

# ╭───────────────────────────────────────────────────────────────────────────╮
# │ Plotting                                                                  │
# ╰───────────────────────────────────────────────────────────────────────────╯

# Define default dimensions of pyplot figures.
FIG_SIZE = CONFIG["plotting"]["fig_size"]

# Define number of simulation-steps between each plot.
STEPS_BETWEEN_PLOT = CONFIG["plotting"]["steps_between_plot"]

# Define theme for pyplot.
MPL_THEME = CONFIG["plotting"]["theme"]
if MPL_THEME == "dark":
    MPL_THEME = "~/.config/matplotlib/dark.mplstyle"
elif MPL_THEME == "light":
    MPL_THEME = None
else:
    MPL_THEME = None

# Define which simulations plots should be created for.
CREATE_PLOTS_FOR = CONFIG["plotting"]["plot_which_runs"]

