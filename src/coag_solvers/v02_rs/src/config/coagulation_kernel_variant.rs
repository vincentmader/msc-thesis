#[derive(Debug)]
pub enum CoagulationKernelVariant {
    Constant,
    Linear,
    Quadratic,
}
impl From<&str> for CoagulationKernelVariant {
    fn from(kernel_variant: &str) -> Self {
        match kernel_variant {
            "constant" => Self::Constant,
            "linear" => Self::Linear,
            "quadratic" => Self::Quadratic,
            _ => todo!(),
        }
    }
}
