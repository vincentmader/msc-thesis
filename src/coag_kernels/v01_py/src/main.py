import sys

from config import Config
from kernel_construction import kernel as K
from utils.cprint import cprint
from utils import file_io


if __name__ == "__main__":
    # Get run-id from command-line argument, and print it.
    run_id = sys.argv[1]
    cprint(f"{run_id}", indent=1, color="cyan")

    # Load configuration from TOML file.
    cfg = Config()

    # Create coagulation kernel.
    kernel = K(cfg)

    # Save kernel to file.
    file_io.save_coagulation_kernel_to_file(cfg, run_id, kernel)
