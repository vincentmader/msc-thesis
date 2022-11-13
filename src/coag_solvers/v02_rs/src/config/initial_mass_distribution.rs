#[derive(Debug)]
pub enum InitialMassDistribution {
    DiracDelta,
    Gaussian,
}
impl From<&str> for InitialMassDistribution {
    fn from(initial_mass_distribution: &str) -> Self {
        match initial_mass_distribution {
            "dirac-delta" => Self::DiracDelta,
            "gaussian" => Self::Gaussian,
            _ => todo!(),
        }
    }
}
