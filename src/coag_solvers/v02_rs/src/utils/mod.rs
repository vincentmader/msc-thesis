pub fn read_file_to_string(path_to_file: &str) -> String {
    let error_msg = format!("ERROR: Couldn't read file at `{}`", path_to_file);
    std::fs::read_to_string(path_to_file).expect(&error_msg)
}

pub fn load_toml_from_string(toml_string: &str) -> toml::Value {
    toml_string.parse::<toml::Value>().unwrap()
}

pub fn load_config() -> toml::Value {
    let cfg = "../../../config.toml";
    let cfg = read_file_to_string(cfg);
    let cfg = load_toml_from_string(&cfg);
    cfg
}
