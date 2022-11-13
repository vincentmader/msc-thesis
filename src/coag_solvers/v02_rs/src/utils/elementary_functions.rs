use std::f64::consts::PI;

pub fn gaussian(x: &Vec<f64>, mu: f64, sigma: f64) -> Vec<f64> {
    let f = |x: f64| (-(x - mu) / sigma.powf(2.)).exp() / ((2. * PI).powf(0.5) * sigma);
    x.iter().map(|x| f(*x)).collect()
}

pub fn dirac_delta(x: &Vec<f64>, i_0: usize) -> Vec<f64> {
    let f = |i: usize| match i == i_0 {
        true => 1_f64,
        false => 0_f64,
    };
    (0..x.len()).map(|i| f(i)).collect()
}

pub fn kronecker_delta(i: i32, j: i32) -> i32 {
    match i == j {
        true => 1,
        false => 0,
    }
}
