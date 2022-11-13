use crate::utils;

pub fn load_config() -> toml::Value {
    let cfg = "../../../config.toml";
    let cfg = utils::file_io::read_file_to_string(cfg);
    let cfg = utils::file_io::load_toml_from_string(&cfg);
    cfg
}
