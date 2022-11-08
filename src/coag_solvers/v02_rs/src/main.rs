use v02_rs::utils;

fn main() {
    println!("Running solver v02_rs...");
    let cfg = utils::load_config();

    println!("{:?}", cfg);

    // let a = &cfg["solver"]["version"];
}
