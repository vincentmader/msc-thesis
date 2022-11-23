from numpy import float64 as f64
import toml


class Config:
    def __init__(self):
        cfg = toml.load("./config.toml")

        # ╭───────────────────────────────────────────────────────────────────╮
        # │ Solver                                                            │
        # ╰───────────────────────────────────────────────────────────────────╯

        # Specify whether solver should be run.
        # NOTE: Initialization will always take place.
        run_solver = cfg["solver"]["run_solver"]

        # Define maximum length for run-id. (e.g. 8 -> max. 10^8 runs)
        max_run_id_length = cfg["solver"]["max_run_id_length"]

        # ╭───────────────────────────────────────────────────────────────────╮
        # │ Mass Grid                                                         │
        # ╰───────────────────────────────────────────────────────────────────╯

        # Define number of points in mass-grid.
        mass_grid_resolution = cfg["mass_grid"]["mass_grid_resolution"]

        # Define minimum & maximum exponent of logarithmic mass-grid.
        mass_grid_exp_min = f64(cfg["mass_grid"]["mass_grid_exp_min"])
        mass_grid_exp_max = f64(cfg["mass_grid"]["mass_grid_exp_max"])

        # Define (multiplicative) step-size from one mass-grid-point to the next.
        range_of_scales = 10**(mass_grid_exp_max - mass_grid_exp_min)
        mass_grid_stepsize = range_of_scales**(1 / mass_grid_resolution)

        # ╭───────────────────────────────────────────────────────────────────╮
        # │ Coagulation Kernel                                                │
        # ╰───────────────────────────────────────────────────────────────────╯

        # Define variant of coagulation kernel.
        coagulation_kernel_variant = cfg["coagulation_kernel"]["variant"]

        # ╭───────────────────────────────────────────────────────────────────╮
        # │ Initialization                                                    │
        # ╰───────────────────────────────────────────────────────────────────╯

        # Define the initial state.
        initial_mass_distribution = cfg["initialization"]["initial_mass_distribution"]

        # ╭───────────────────────────────────────────────────────────────────╮
        # │ Simulation                                                        │
        # ╰───────────────────────────────────────────────────────────────────╯

        # Define Discretization of Time-Axis (Abscissa).
        nr_of_timesteps = cfg["simulation"]["nr_of_timesteps"]

        # Define size of multiplicative time-step.
        multiplicative_dt = cfg["simulation"]["multiplicative_dt"]

        # Determine whether near-zero-cancellation should be handled.
        handle_near_zero_cancellation = cfg["simulation"]["handle_near_zero_cancellation"]

        # ╭───────────────────────────────────────────────────────────────────╮
        # │ File-IO                                                           │
        # ╰───────────────────────────────────────────────────────────────────╯

        # Define path to configuration TOML file.
        path_to_config = cfg["file_io"]["path_to_config"]

        # Define path to directory where figures shall be saved.
        path_to_outfiles = cfg["file_io"]["path_to_outfiles"]

        # ╭───────────────────────────────────────────────────────────────────╮
        # │ Testing                                                           │
        # ╰───────────────────────────────────────────────────────────────────╯

        # Determine whether to run stability tests.
        run_stability_tests = cfg["testing"]["run_stability_tests"]

        # ╭───────────────────────────────────────────────────────────────────╮
        # │ Plotting                                                          │
        # ╰───────────────────────────────────────────────────────────────────╯

        # Define default dimensions for pyplot figures.
        default_fig_size = cfg["plotting"]["default_fig_size"]

        # Define number of simulation-steps between each plot.
        steps_between_plot = cfg["plotting"]["steps_between_plot"]

        # Define theme for pyplot.
        mpl_theme = cfg["plotting"]["theme"]
        if mpl_theme == "dark":
            mpl_theme = "~/.config/matplotlib/dark.mplstyle"
        elif mpl_theme == "light":
            mpl_theme = None
        else:
            mpl_theme = None

        # Define which simulations plots should be created for.
        runs_to_plot = cfg["plotting"]["runs_to_plot"]

        # Define which plots should be created.
        plots_to_create = cfg["plotting"]["plots_to_create"]

        # Define which plots should be shown immediately.
        plots_to_show = cfg["plotting"]["plots_to_show"]

        # ─────────────────────────────────────────────────────────────────────

        self.run_solver = run_solver
        self.max_run_id_length = max_run_id_length
        self.mass_grid_resolution = mass_grid_resolution
        self.mass_grid_exp_min = mass_grid_exp_min
        self.mass_grid_exp_max = mass_grid_exp_max
        self.mass_grid_stepsize = mass_grid_stepsize
        self.coagulation_kernel_variant = coagulation_kernel_variant
        self.initial_mass_distribution = initial_mass_distribution
        self.nr_of_timesteps = nr_of_timesteps
        self.multiplicative_dt = multiplicative_dt
        self.handle_near_zero_cancellation = handle_near_zero_cancellation
        self.path_to_config = path_to_config
        self.path_to_outfiles = path_to_outfiles
        self.default_fig_size = default_fig_size
        self.steps_between_plot = steps_between_plot
        self.mpl_theme = mpl_theme
        self.runs_to_plot = runs_to_plot
        self.plots_to_create = plots_to_create
        self.plots_to_show = plots_to_show
        self.run_stability_tests = run_stability_tests
