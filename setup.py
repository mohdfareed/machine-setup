#!/usr/bin/env python3

from core import ssh
from utils import shell
from utils.display import Display


def setup(display: Display, ssh_dir: str) -> None:
    """Run the main function of the setup script. This function is called when
    the script is run from the command line.

    Args:
        display (Display): The display for printing messages.
        ssh_dir (str): The path to the SSH directory of keys.
    """
    display.header("Setting up machine...")

    # setup ssh keys if not already present
    ssh.setup(ssh_dir, display, quiet=True)

    # get resources if not already present
    display.debug("Initializing resources...")
    cmd = "git submodule update --init --recursive --remote"
    if shell.run_quiet(cmd, display.verbose, "Initializing resources") != 0:
        raise RuntimeError("Failed to initialize resources.")
    display.success("Resources initialized.")

    # run setup modules
    display.debug("Running setup modules...")
    _invoke_setup(display)
    display.success("")
    display.success("Machine setup complete!")
    display.info("Please restart your machine for some changes to apply.")


def main() -> None:
    """Initialize the Display and run the main setup function."""
    import argparse

    # parse command line arguments
    parser = argparse.ArgumentParser(description="Machine setup script.")
    parser.add_argument(
        "--ssh-dir",
        type=str,
        required=True,
        help="the path to the ssh directory of keys",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print verbose messages, including commands",
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="print debug messages"
    )
    parser.add_argument(
        "--no-logging", action="store_true", help="don't log output to a file"
    )
    args = parser.parse_args()

    # create a display instance for logging and printing messages
    verbose, debug, no_logging = args.verbose, args.debug, args.no_logging
    display = _init(verbose, debug, no_logging)

    try:  # run main function and handle exceptions
        setup(display, args.ssh_dir)
    except Exception as exception:
        display.error(exception.__str__())
        display.error("")
        display.error(f"Failed to setup machine.")


def _init(verbose, debug, no_logging) -> Display:
    """Initialize display for printing messages and logging them to a file."""
    display = Display(verbose, debug, no_logging)
    display.debug("Debug mode is enabled.") if debug else None
    display.verbose("Verbose mode is enabled.") if verbose else None
    display.info("Logging is disabled.") if no_logging else None
    return display


def _invoke_setup(display: Display) -> None:
    """Invoke the setup modules.

    Args:
        display (Display): The display for printing messages.
    """
    from core import git, homebrew, macos, python, zsh

    homebrew.setup(display)
    zsh.setup(display)
    git.setup(display)
    python.setup(display)
    macos.setup(display)


if __name__ == "__main__":
    main()
