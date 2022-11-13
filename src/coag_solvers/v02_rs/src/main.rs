use v02_rs::config::Config;

fn run_solver(cfg: &Config) {
    for _t in 0..cfg.nr_of_timesteps {
        //
    }
}

fn main() {
    println!("Running solver v02_rs...");

    // Load configuration TOML file.
    let cfg = Config::new();

    // Run coagulation solver.
    run_solver(&cfg);
}
