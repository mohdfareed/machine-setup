#!/usr/bin/env python3

from setup_modules import git, homebrew, macos, python, ssh, zsh
from utils import abs_path, shell
from utils.display import Display


def main(display: Display, ssh_dir: str) -> None:
    """Run the main function of the setup script. This function is called when
    the script is run from the command line. It will prompt the user to run
    a setup function for every setup module. By default, the setup is run in
    verbose and debug mode without logging output to a file.

    Args:
        display (Display): The display for printing messages.
        ssh_dir (str): The path to the SSH directory of keys.
    """
    display.header("Setting up machine...")

    # setup ssh keys if not already present
    ssh.setup(ssh_dir, display, quiet=True)

    # get resources if not already present
    display.debug("Initializing resources...")
    cmd = 'git submodule update --init --recursive --remote'
    if shell.run_quiet(cmd, display.verbose, "Initializing resources") != 0:
        raise RuntimeError("Failed to initialize resources.")
    display.success("Resources initialized.")

    # prompt user to setup components
    display.debug("Running setup modules...")
    homebrew.setup(display)
    zsh.setup(display)
    git.setup(display)
    python.setup(display)
    macos.setup(display)

    display.success("")
    display.success("Machine setup complete!")
    display.info("Please restart your machine for some changes to apply.")


def _init(verbose, debug, no_logging) -> Display:
    """Initialize the display for printing messages and logging them to a file.
    """
    display = Display(verbose, debug, no_logging)
    display.debug("Debug mode is enabled.") if debug else None
    display.verbose("Verbose mode is enabled.") if verbose else None
    display.info("Logging is disabled.") if no_logging else None
    return display


if __name__ == "__main__":
    import argparse

    # parse command line arguments
    parser = argparse.ArgumentParser(description="Machine setup script.")
    parser.add_argument("--ssh-dir", type=str, required=True,
                        help="the path to the ssh directory of keys")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print verbose messages, including commands")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="print debug messages")
    parser.add_argument("--no-logging", action="store_true",
                        help="don't log output to a file")
    args = parser.parse_args()

    # create a display instance for logging and printing messages
    verbose, debug, no_logging = args.verbose, args.debug, args.no_logging
    display = _init(verbose, debug, no_logging)

    try:  # run main function and handle exceptions
        main(display, args.ssh_dir)
    except Exception as exception:
        display.error(exception.__str__())
        display.error("")
        display.error(f"Failed to setup machine.")
