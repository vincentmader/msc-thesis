from numpy import float64 as f64
import toml


CONFIG = toml.load("./config.toml")

# ╭───────────────────────────────────────────────────────────────────────────╮
# │ Solver                                                                    │
# ╰───────────────────────────────────────────────────────────────────────────╯

# Define variant of solver.
# Trivial: -> Python (v01)

# Define maximum length for run-id. (e.g. 8 -> max. 10^8 runs)
MAX_RUN_ID_LENGTH = CONFIG["solver"]["max_run_id_length"]

# ╭───────────────────────────────────────────────────────────────────────────╮
# │ Mass Grid                                                                 │
# ╰───────────────────────────────────────────────────────────────────────────╯

# Define number of points in mass-grid.
GRID_RESOLUTION = CONFIG["mass_grid"]["mass_grid_resolution"]

# Define minimum & maximum exponent of logarithmic mass-grid.
GRID_EXP_MIN = f64(CONFIG["mass_grid"]["mass_grid_exp_min"])
GRID_EXP_MAX = f64(CONFIG["mass_grid"]["mass_grid_exp_max"])

# Define (multiplicative) step-size from one mass-grid-point to the next.
GRID_STEPSIZE = (10**(GRID_EXP_MAX-GRID_EXP_MIN))**(1/GRID_RESOLUTION)

# ╭───────────────────────────────────────────────────────────────────────────╮
# │ Kernel                                                                    │
# ╰───────────────────────────────────────────────────────────────────────────╯

# Define variant of coagulation kernel.
COAGULATION_KERNEL_VARIANT = CONFIG["coagulation_kernel"]["variant"]

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

# Determine whether near-zero-cancellation should be handled.
HANDLE_NEAR_ZERO_CANCELLATION = CONFIG["simulation"]["handle_near_zero_cancellation"]

# ╭───────────────────────────────────────────────────────────────────────────╮
# │ File-IO                                                                   │
# ╰───────────────────────────────────────────────────────────────────────────╯

# Define path to configuration TOML file.
PATH_TO_CONFIG = CONFIG["file_io"]["path_to_config"]

# Define path to directory where figures shall be saved.
PATH_TO_OUTFILES = CONFIG["file_io"]["path_to_outfiles"]

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
RUNS_TO_PLOT = CONFIG["plotting"]["runs_to_plot"]

# Define which plots should be created.
PLOTS_TO_CREATE = CONFIG["plotting"]["plots_to_create"]

# Define which plots should be shown immediately.
PLOTS_TO_SHOW = CONFIG["plotting"]["plots_to_show"]
