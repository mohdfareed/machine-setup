#!/usr/bin/env python3

from core import git, macos, python, raspberrypi, shell, ssh
from utils import shell
from utils.display import Display


def main(config_path: str, log=False, debug=False) -> None:
    """Setup the machine.

    Args:
        config_path (str): Path to the local config directory.
        log (bool): Whether to log output to a file.
        debug (bool): Whether to log debug messages.
    """

    setup_logging(to_file=log, debug=debug)
    setup_display()

    try:  # run main function and handle exceptions
        setup_machine(display, args.ssh_dir)
    except Exception as exception:
        display.error(exception.__str__())
        display.error("")
        display.error(f"Failed to setup machine.")

    print("[bold green]chatgpt_bot stopped[/]")


def setup_logging(to_file, debug):
    # configure logging
    logging.captureWarnings(True)
    root_logger = logging.getLogger()
    root_logger.level = logging.WARNING  # default level

    # set up logging level for all modules
    level = logging.DEBUG if debug else logging.INFO
    for module in LOGGING_MODULES:
        logging.getLogger(module).setLevel(level)
    # set up logging level for this module
    (local_logger := logging.getLogger(__name__)).setLevel(level)

    if not to_file:  # set up logging to file
        return
    local_logger.debug("Debug mode enabled")
    format = (
        "[%(asctime)s] %(levelname)-8s "
        "%(message)s - %(name)s [%(filename)s:%(lineno)d]"
    )

    # create file handler
    logging_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(logging_dir, exist_ok=True)
    filename = f"{datetime.now():%y%m%d_%H%M%S}.log"
    file = os.path.join(logging_dir, filename)
    file_handler = logging.FileHandler(file)
    formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S")

    # setup handler
    logger.addHandler(file_handler)
    file_handler.setFormatter(formatter)
    logger.info(f"Logging to file: {file}")


def setup_machine(display: Display, ssh_dir: str | None) -> None:
    """Run the main function of the setup script. This function is called when
    the script is run from the command line.

    Args:
        display (Display): The display for printing messages.
        ssh_dir (str): The path to the SSH directory of keys.
    """
    display.header("Setting up machine...")

    # setup ssh keys if not already present
    if ssh_dir is not None:
        ssh.setup(ssh_dir, display, quiet=True)

    # get resources if not already present
    display.debug("Initializing resources...")
    cmd = "git submodule update --init --recursive --remote"
    if shell.run_quiet(cmd, display.verbose, "Initializing resources") != 0:
        raise RuntimeError("Failed to initialize resources.")
    display.success("Resources initialized.")

    # run setup scripts
    # homebrew.setup(display)
    # zsh.setup(display)
    # git.setup(display)
    # python.setup(display)
    # macos.setup(display)
    raspberrypi.setup(display)
    display.success("Machine setup complete!")
    display.info("Restart machine for some changes to apply.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Setup machine.")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="start in debug mode"
    )
    parser.add_argument(
        "-l", "--log", action="store_true", help="log to a file"
    )
    parser.add_argument(
        "config_path", type=str, help="local machine config path"
    )

    args = parser.parse_args()
    main(args.config_path, args.log, args.debug)
