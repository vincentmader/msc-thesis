#![allow(unused_imports)]

use v02_rs::config::Config;
use v02_rs::state_forwarding;
use v02_rs::state_initialization;

fn run_solver(cfg: &Config) {
    for _t in 0..cfg.nr_of_timesteps {
        //
    }
}

fn main() {
    println!("Running solver v02_rs...");

    // Load configuration TOML file.
    let cfg = Config::new();

    // Define coagulation kernel & initial state of disk's mass distribution.
    // ────────────────────────────────────────────────────────────────────────

    // Define coagulation kernel (gain & loss terms, separately).
    // TODO

    // Define initial state.
    // TODO

    // Run coagulation solver.
    // ────────────────────────────────────────────────────────────────────────

    // Compute time-evolution of mass distribution
    // (& TODO record execution time).
    run_solver(&cfg);

    // Save to file.
    // ────────────────────────────────────────────────────────────────────────

    // TODO
}
