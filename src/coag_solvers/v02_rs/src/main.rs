#![allow(unused_imports)]

use v02_rs::config::initial_mass_distribution::InitialMassDistribution;
use v02_rs::config::Config;
use v02_rs::state_forwarding;
use v02_rs::state_initialization;
use v02_rs::utils::elementary_functions;

struct DiskState {
    mass_distribution: Vec<f64>,
}

impl DiskState {
    pub fn new(cfg: &Config) -> Self {
        // Load information about mass grid abscissa from configuration.
        let mass_grid_resolution = &cfg.mass_grid_resolution;
        let mass_grid_exp_min = &cfg.mass_grid_exp_min;
        let mass_grid_stepsize = &cfg.mass_grid_stepsize;

        // Define mass grid abscissa.
        let mass_grid: Vec<f64> = (0..*mass_grid_resolution)
            .map(|i| mass_grid_exp_min * mass_grid_stepsize.powf(i as f64))
            .collect();

        // Load information about initial mass distribution from configuration.
        let initial_mass_distribution = &cfg.initial_mass_distribution;

        // Define initial mass distribution.
        let i_0 = 1; // TODO move
        let mu = 1.; // TODO move
        let sigma = 1.; // TODO move
        let initial_mass_distribution: Vec<f64> = match initial_mass_distribution {
            InitialMassDistribution::DiracDelta => {
                elementary_functions::dirac_delta(&mass_grid, i_0)
            }
            InitialMassDistribution::Gaussian => {
                elementary_functions::gaussian(&mass_grid, mu, sigma)
            }
        };

        // Return disk state.
        let mass_distribution = initial_mass_distribution;
        DiskState { mass_distribution }
    }

    pub fn forward(&self) -> Self {
        let mass_distribution = self.mass_distribution.clone();
        // TODO forward to next time step
        DiskState { mass_distribution }
    }
}

fn run_solver(cfg: &Config, initial_disk_state: DiskState) {
    // Define vector holding disk states at all times.
    let mut disk_states = vec![initial_disk_state];

    // Run compute loop.
    for t in 0..cfg.nr_of_timesteps {
        // Load current disk state from vector.
        let disk_state = &disk_states[t];

        // Compute next disk state.
        let next_state = disk_state.forward();

        // Append to state vector.
        disk_states.push(next_state);
    }
}

fn main() {
    println!("Running solver v02_rs...");

    // Load solver configuration from TOML file.
    let cfg = Config::new();

    // Define coagulation kernel & initial state of disk's mass distribution.
    // ────────────────────────────────────────────────────────────────────────

    // Define coagulation kernel (gain & loss terms, separately).
    // TODO

    // Define initial state.
    let initial_disk_state = DiskState::new(&cfg);

    // Run coagulation solver.
    // ────────────────────────────────────────────────────────────────────────

    // Compute time-evolution of mass distribution
    // (& TODO record execution time).
    if cfg.run_solver {
        run_solver(&cfg, initial_disk_state);
    }

    // Save to file.
    // ────────────────────────────────────────────────────────────────────────

    // TODO
}
