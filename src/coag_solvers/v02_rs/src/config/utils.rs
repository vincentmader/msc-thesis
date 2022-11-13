use crate::utils;

pub fn load_config() -> toml::Value {
    let cfg = "../../../config.toml";
    let cfg = utils::read_file_to_string(cfg);
    let cfg = utils::load_toml_from_string(&cfg);
    cfg
}
