from numpy import log10
from numpy import float64 as f64
import toml


class Config:
    def __init__(self):
        cfg = toml.load("./config.toml")

        # ╭───────────────────────────────────────────────────────────────────╮
        # │ Time Discretization                                               │
        # ╰───────────────────────────────────────────────────────────────────╯
        section = cfg["time_discretization"]

        # Define discretization of Time-Axis (Abscissa).
        nr_of_timesteps = section["nr_of_timesteps"]
        # Specify type of time-step incrementation.
        dt_incrementation = section["dt_incrementation"]
        # Define size of additive time-step.
        additive_dt = section["additive_dt"]
        # Define size of multiplicative time-step.
        multiplicative_dt = section["multiplicative_dt"]

        # ╭───────────────────────────────────────────────────────────────────╮
        # │ Mass Discretization                                               │
        # ╰───────────────────────────────────────────────────────────────────╯
        section = cfg["mass_discretization"]

        # Define mass-grid variant.
        mass_grid_variant = section["mass_grid_variant"]
        # Define number of points in mass-grid.
        mass_grid_resolution = section["mass_grid_resolution"]
        # Define minimum & maximum exponent of logarithmic mass-grid.
        mass_grid_min = f64(section["minimum_mass"])
        mass_grid_max = f64(section["maximum_mass"])
        if mass_grid_variant == "linear":
            # Define additive step-size from one grid-point to the next.
            raise Exception()
        elif mass_grid_variant == "logarithmic":
            # Define multiplicative step-size from one grid-point to the next.
            range_of_scales = 10**(mass_grid_max - mass_grid_min)
            mass_grid_stepsize = range_of_scales**(1 / (mass_grid_resolution-1))
        else:
            raise Exception()

        # ╭───────────────────────────────────────────────────────────────────╮
        # │ Coagulation Kernel                                                │
        # ╰───────────────────────────────────────────────────────────────────╯
        section = cfg["coagulation_kernel"]

        # Define variant of coagulation kernel.
        coagulation_kernel_variant = section["variant"]

        # ╭───────────────────────────────────────────────────────────────────╮
        # │ Stability                                                         │
        # ╰───────────────────────────────────────────────────────────────────╯
        section = cfg["stability"]

        # Determine whether near-zero-cancellation should be handled.
        handle_near_zero_cancellation = section["handle_near_zero_cancellation"]

        # ╭───────────────────────────────────────────────────────────────────╮
        # │ Initialization                                                    │
        # ╰───────────────────────────────────────────────────────────────────╯
        section = cfg["initialization"]

        # Define the initial state.
        initial_mass_distribution = section["initial_mass_distribution"]

        # ╭───────────────────────────────────────────────────────────────────╮
        # │ Testing                                                           │
        # ╰───────────────────────────────────────────────────────────────────╯
        section = cfg["testing"]

        # Determine whether to run stability tests.
        run_stability_tests = section["run_stability_tests"]

        # ╭───────────────────────────────────────────────────────────────────╮
        # │ Plotting                                                          │
        # ╰───────────────────────────────────────────────────────────────────╯
        section = cfg["plotting"]

        # Define default dimensions for pyplot figures.
        default_fig_size = section["default_fig_size"]
        # Define number of simulation-steps between each plot.
        steps_between_plot = section["steps_between_plot"]
        # Define theme for pyplot.
        mpl_theme = section["theme"]
        if mpl_theme == "dark":
            mpl_theme = "~/.config/matplotlib/dark.mplstyle"
        elif mpl_theme == "light":
            mpl_theme = None
        else:
            mpl_theme = None
        # Define which simulations plots should be created for.
        runs_to_plot = section["runs_to_plot"]
        # Define which plots should be created.
        plots_to_create = section["plots_to_create"]
        # Define which plots should be shown immediately.
        plots_to_show = section["plots_to_show"]

        # ╭───────────────────────────────────────────────────────────────────╮
        # │ Project                                                           │
        # ╰───────────────────────────────────────────────────────────────────╯
        section = cfg["project"]

        kernel_version = section["kernel_version"]
        solver_version = section["solver_version"]

        # ╭───────────────────────────────────────────────────────────────────╮
        # │ Solver                                                            │
        # ╰───────────────────────────────────────────────────────────────────╯
        section = cfg["solver"]

        # Specify whether solver should be run.
        # NOTE: Initialization will always take place.
        run_solver = section["run_solver"]

        # ╭───────────────────────────────────────────────────────────────────╮
        # │ File-IO                                                           │
        # ╰───────────────────────────────────────────────────────────────────╯
        section = cfg["file_io"]

        # Define maximum length for run-id. (e.g. 8 -> max. 10^8 runs)
        max_run_id_length = section["max_run_id_length"]
        # Define path to configuration TOML file.
        path_to_config = section["path_to_config"]
        # Define path to directory where figures shall be saved.
        path_to_outfiles = section["path_to_outfiles"]

        # ─────────────────────────────────────────────────────────────────────

        self.additive_dt = additive_dt
        self.coagulation_kernel_variant = coagulation_kernel_variant
        self.default_fig_size = default_fig_size
        self.dt_incrementation = dt_incrementation
        self.handle_near_zero_cancellation = handle_near_zero_cancellation
        self.initial_mass_distribution = initial_mass_distribution
        self.kernel_version = kernel_version
        self.mass_grid_min = mass_grid_min
        self.mass_grid_max = mass_grid_max
        self.mass_grid_variant = mass_grid_variant
        # self.mass_grid_exp_max = mass_grid_exp_max
        # self.mass_grid_exp_min = mass_grid_exp_min
        self.mass_grid_resolution = mass_grid_resolution
        self.mass_grid_stepsize = mass_grid_stepsize
        self.max_run_id_length = max_run_id_length
        self.mpl_theme = mpl_theme
        self.multiplicative_dt = multiplicative_dt
        self.nr_of_timesteps = nr_of_timesteps
        self.path_to_config = path_to_config
        self.path_to_outfiles = path_to_outfiles
        self.plots_to_create = plots_to_create
        self.plots_to_show = plots_to_show
        self.run_solver = run_solver
        self.run_stability_tests = run_stability_tests
        self.runs_to_plot = runs_to_plot
        self.solver_version = solver_version
        self.steps_between_plot = steps_between_plot
