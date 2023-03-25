#!/usr/bin/env python3

from setup_modules import homebrew, git, zsh, python, macos
from utils.display import Display
from utils.shell import Shell
from typing import Callable
import os

silent: bool = False
"""Do not prompt the user during setup."""
no_logging: bool = True
"""Do not log output to a file."""
verbose: bool = True
"""Print verbose output."""
debug: bool = True
"""Print debug output."""


def main() -> None:
    """Run the main function of the setup script. This function is called when
    the script is run from the command line. It will prompt the user to run
    a setup function for every setup module. By default, the setup is run in
    verbose and debug mode without logging output to a file."""
    # set the working directory to the directory of this file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    display, shell = _init()  # initialize display and shell
    display.header("Setting up machine...")

    # check if git is installed
    if shell.run('command -v git', display.debug, display.error) != 0:
        display.error("Git is not installed.")
        exit(1)
    display.verbose("Git installation found.")

    # get resources if not already present
    if shell.run_quiet('git submodule update --init --recursive --remote',
                       display.verbose, "Initializing resources") != 0:
        display.error("Failed to initialize resources.")
        exit(1)
    display.success("Resources initialized.")

    # prompt user to setup components
    _prompt_setup(homebrew.setup, "Homebrew", display, shell)
    _prompt_setup(zsh.setup, "Zsh", display, shell)
    _prompt_setup(git.setup, "Git", display, shell)
    _prompt_setup(python.setup, "Python", display, shell)
    _prompt_setup(macos.setup, "macOS", display, shell)

    # inform user that setup is complete and a restart is required
    display.success("")
    display.success("Machine setup complete!")
    display.info("Please restart your machine for some changes to apply.")


def _init() -> tuple[Display, Shell]:
    """Initialize a `Display` and `Shell` for the setup script and prints the
    display mode. If the script is run in silent mode, it will prompt the user
    for their password to get sudo privileges.

    Returns:
        tuple[Display, Shell]: A list containing the `Display` and `Shell`.
    """

    # create a shell instance and set display mode
    display = Display(verbose, debug, no_logging)
    shell = Shell()
    # print setup display mode
    display.debug("Debug mode is enabled.") if debug else None
    display.verbose("Verbose mode is enabled.") if verbose else None
    display.info("Logging is disabled.") if no_logging else None
    if not silent:
        return display, shell

    # prompt user for sudo privileges if running in silent mode
    display.warning("Silent mode is enabled.")
    display.header("Sudo privileges are required to run in silent mode.")
    # create a shell instance with sudo privileges
    try:
        shell = Shell(sudo=True)
    except PermissionError:
        display.error("Failed to get sudo privileges.")
        exit(1)
    display.verbose("Sudo privileges granted.")

    return display, shell


def _prompt_setup(procedure: Callable, name: str,
                  display: Display, shell: Shell) -> None:
    """Prompt the user to run a setup procedure with a `Display` object. It
    will run the procedure if the user enters "y" or "yes". The procedure
    should take a `Display` object as its only argument.

    Args:
        procedure (function): The setup procedure to run.
        display (Display): The display for printing output.
    """
    if silent:
        procedure(display, shell, silent=True)
        return

    answer = input(f"Do you want to setup {name}? (y/n [n]) ")
    if answer and answer.lower()[0] == "y":
        procedure(display, shell)


if __name__ == "__main__":
    import argparse

    # parse command line arguments
    parser = argparse.ArgumentParser(description="Machine setup script.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print verbose messages")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="print debug messages")
    parser.add_argument("--no-log", action="store_true",
                        help="don't log output to a file")
    parser.add_argument("-s", "--silent", action="store_true",
                        help="don't prompt user for input")
    args = parser.parse_args()

    # assign arguments to global variables
    verbose = args.verbose
    debug = args.debug
    no_logging = args.no_log
    silent = args.silent

    # run main function
    main()
