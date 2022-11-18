from termcolor import colored

from config import Config
from utils import mass_from_index, index_from_mass

def test_mass_index_conversion(cfg):
    print("")

    mass_grid_resolution = cfg.mass_grid_resolution
    mass_grid_exp_min = cfg.mass_grid_exp_min
    mass_grid_stepsize = cfg.mass_grid_stepsize

    correct, incorrect = 0, 0
    for i in range(mass_grid_resolution):
        m_i = mass_from_index(i, mass_grid_exp_min, mass_grid_stepsize)
        i_m = index_from_mass(m_i, mass_grid_exp_min, mass_grid_stepsize)

        if i == i_m:
            correct += 1
        else:
            print(f"i={i} != {i_m}=i_m")
            incorrect += 1
    
    total = correct + incorrect
    
    if incorrect == 0:
        msg = f"\nSuccess: All {correct} transformations i->m_i->i correct!"
        print(colored(msg, "green"))
    else:
        msg = f"\nFailure: {incorrect}/{total} transformations were incorrect!"
        print(colored(msg, "red"))


if __name__ == "__main__":
    cfg = Config()

    test_mass_index_conversion(cfg)
