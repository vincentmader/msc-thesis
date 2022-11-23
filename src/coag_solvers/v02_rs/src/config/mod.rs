pub mod coagulation_kernel_variant;
pub mod initial_mass_distribution;
mod utils;

use coagulation_kernel_variant::CoagulationKernelVariant;
use initial_mass_distribution::InitialMassDistribution;

#[derive(Debug)]
pub struct Config {
    pub run_solver: bool,
    pub max_run_id_length: usize,
    pub mass_grid_resolution: usize,
    pub mass_grid_exp_min: f64,
    pub mass_grid_exp_max: f64,
    pub mass_grid_stepsize: f64,
    pub coagulation_kernel_variant: CoagulationKernelVariant,
    pub initial_mass_distribution: InitialMassDistribution,
    pub nr_of_timesteps: usize,
    pub handle_near_zero_cancellation: bool,
    pub path_to_config: Box<std::path::PathBuf>,
    pub path_to_outfiles: Box<std::path::PathBuf>,
}

impl Config {
    pub fn new() -> Self {
        let cfg = utils::load_config();

        // ╭──────────────────────────────────────────────────────────────────╮
        // │ Solver                                                           │
        // ╰──────────────────────────────────────────────────────────────────╯

        // Specify whether solver should be run.
        // NOTE: Initialization will always take place.
        let run_solver = &cfg["solver"]["run_solver"];
        let run_solver = run_solver.as_bool().unwrap();

        // Define maximum length for run-id string. (e.g. 8 -> max. 10^8 runs)
        let max_run_id_length = &cfg["solver"]["max_run_id_length"];
        let max_run_id_length = max_run_id_length.as_integer().unwrap();
        let max_run_id_length = max_run_id_length as usize;

        // ╭──────────────────────────────────────────────────────────────────╮
        // │ Mass Grid                                                        │
        // ╰──────────────────────────────────────────────────────────────────╯

        // Specify minimum mass exponent.
        let mass_grid_exp_min = &cfg["mass_grid"]["mass_grid_exp_min"];
        let mass_grid_exp_min = mass_grid_exp_min.as_integer().unwrap();
        let mass_grid_exp_min = mass_grid_exp_min as f64;

        // Specify maximum mass exponent.
        let mass_grid_exp_max = &cfg["mass_grid"]["mass_grid_exp_max"];
        let mass_grid_exp_max = mass_grid_exp_max.as_integer().unwrap();
        let mass_grid_exp_max = mass_grid_exp_max as f64;

        // Specify mass grid resolution.
        let mass_grid_resolution = &cfg["mass_grid"]["mass_grid_resolution"];
        let mass_grid_resolution = mass_grid_resolution.as_integer().unwrap() as usize;

        // Define (multiplicative) step-size from one mass-grid-point to the next.
        let mass_grid_stepsize = 10_f64.powf(mass_grid_exp_max - mass_grid_exp_min);
        let mass_grid_stepsize = mass_grid_stepsize.powf(1. / mass_grid_resolution as f64);

        // ╭──────────────────────────────────────────────────────────────────╮
        // │ Coagulation Kernel                                               │
        // ╰──────────────────────────────────────────────────────────────────╯

        // Define coagulation kernel variant.
        let coagulation_kernel_variant = &cfg["coagulation_kernel"]["variant"];
        let coagulation_kernel_variant = coagulation_kernel_variant.as_str().unwrap();
        let coagulation_kernel_variant = CoagulationKernelVariant::from(coagulation_kernel_variant);

        // ╭──────────────────────────────────────────────────────────────────╮
        // │ Initialization                                                   │
        // ╰──────────────────────────────────────────────────────────────────╯

        // Define shape of initial mass distribution.
        let initial_mass_distribution = &cfg["initialization"]["initial_mass_distribution"];
        let initial_mass_distribution = initial_mass_distribution.as_str().unwrap();
        let initial_mass_distribution = InitialMassDistribution::from(initial_mass_distribution);

        // ╭──────────────────────────────────────────────────────────────────╮
        // │ Simulation                                                       │
        // ╰──────────────────────────────────────────────────────────────────╯

        // Specify nr. of time-steps.
        let nr_of_timesteps = &cfg["simulation"]["nr_of_timesteps"];
        let nr_of_timesteps = nr_of_timesteps.as_integer().unwrap() as usize;

        // Define size of multiplicative time-step.
        let multiplicative_dt = &cfg["simulation"]["multiplicative_dt"];
        let multiplicative_dt = multiplicative_dt.as_float().unwrap();

        // Determine whether near-zero-cancellation should be handled.
        let handle_near_zero_cancellation = &cfg["simulation"]["handle_near_zero_cancellation"];
        let handle_near_zero_cancellation = handle_near_zero_cancellation.as_bool().unwrap();

        // ╭──────────────────────────────────────────────────────────────────╮
        // │ Plotting                                                         │
        // ╰──────────────────────────────────────────────────────────────────╯

        // Determine whether to run stability tests.
        let run_stability_tests = &cfg["testing"]["run_stability_tests"];
        let run_stability_tests = run_stability_tests.as_bool().unwrap();

        // ╭──────────────────────────────────────────────────────────────────╮
        // │ File-IO                                                          │
        // ╰──────────────────────────────────────────────────────────────────╯

        // Define path to configuration TOML file.
        let path_to_config = &cfg["file_io"]["path_to_config"];
        let path_to_config = path_to_config.as_str().unwrap();
        let path_to_config = std::path::Path::new(path_to_config).to_owned();
        let path_to_config = Box::new(path_to_config);

        // Define path to directory where data & figures should be saved to.
        let path_to_outfiles = &cfg["file_io"]["path_to_outfiles"];
        let path_to_outfiles = path_to_outfiles.as_str().unwrap();
        let path_to_outfiles = std::path::Path::new(path_to_outfiles).to_owned();
        let path_to_outfiles = Box::new(path_to_outfiles);

        // ────────────────────────────────────────────────────────────────────

        Config {
            run_solver,
            max_run_id_length,
            mass_grid_resolution,
            mass_grid_exp_min,
            mass_grid_exp_max,
            mass_grid_stepsize,
            coagulation_kernel_variant,
            initial_mass_distribution,
            nr_of_timesteps,
            handle_near_zero_cancellation,
            path_to_config,
            path_to_outfiles,
            run_stability_tests,
        }
    }
}
