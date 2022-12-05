import sys

from config import Config
from kernel import K
import utils


if __name__ == "__main__":
    # Get run-id from command-line argument.
    run_id = sys.argv[1]

    # Load configuration from TOML file.
    cfg = Config()

    # Create coagulation kernel. 
    kernel = K(cfg)

    # Save kernel to file.
    utils.file_io.save_coagulation_kernel_to_file(cfg, run_id, kernel)
