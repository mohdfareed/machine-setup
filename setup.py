#!/usr/bin/env python3

import os
from typing import Callable

from setup_modules import git, homebrew, macos, python, zsh
from utils.display import Display
from utils.shell import Shell

silent: bool = False
"""Do not prompt the user during setup."""
no_logging: bool = True
"""Do not log output to a file."""
verbose: bool = True
"""Print verbose output."""
debug: bool = True
"""Print debug output."""

_display: Display
"""The display for printing messages."""
_shell: Shell
"""The shell for running commands."""


def main() -> None:
    """Run the main function of the setup script. This function is called when
    the script is run from the command line. It will prompt the user to run
    a setup function for every setup module. By default, the setup is run in
    verbose and debug mode without logging output to a file."""
    global _display, _shell

    # set the working directory to the directory of this file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    _init()  # initialize display and shell
    _display.header("Setting up machine...")

    # check if git is installed
    if _shell.run('command -v git', _display.debug, _display.error) != 0:
        _display.error("Git is not installed.")
        exit(1)
    _display.verbose("Git installation found.")

    # get resources if not already present
    if _shell.run_quiet('git submodule update --init --recursive --remote',
                        _display.verbose, "Initializing resources") != 0:
        _display.error("Failed to initialize resources.")
        exit(1)
    _display.success("Resources initialized.")

    # prompt user to setup components
    _prompt_setup(homebrew.setup, "Homebrew")
    _prompt_setup(zsh.setup, "Zsh")
    _prompt_setup(git.setup, "Git")
    _prompt_setup(python.setup, "Python")
    _prompt_setup(macos.setup, "macOS")

    _display.success("")
    _display.success("Machine setup complete!")
    _display.info("Please restart your machine for some changes to apply.")


def _init():
    """Initialize the `Display` and `Shell` for the setup script and prints the
    display mode. If the script is run in silent mode, it will prompt the user
    for their password to get sudo privileges.
    """
    global silent, no_logging, verbose, debug, _display, _shell

    # create a shell instance and set display mode
    _display = Display(verbose, debug, no_logging)
    _shell = Shell()
    # print setup display mode
    _display.debug("Debug mode is enabled.") if debug else None
    _display.verbose("Verbose mode is enabled.") if verbose else None
    _display.info("Logging is disabled.") if no_logging else None
    if not silent:
        return

    # prompt user for sudo privileges if running in silent mode
    _display.warning("Silent mode is enabled.")
    _display.header("Sudo privileges are required to run in silent mode.")
    # create a shell instance with sudo privileges
    try:
        _shell = Shell(sudo=True)
    except PermissionError:
        _display.error("Failed to get sudo privileges.")
        exit(1)
    _display.verbose("Sudo privileges granted.")


def _prompt_setup(setup: Callable, name: str):
    """Prompt the user to run a setup procedure with a `Display` object. It
    will run the procedure if the user enters "y" or "yes". The procedure
    should take a `Display` object as its only argument.

    Args:
        setup (function): The setup function to run.
        name (str): The name of the setup function.
    """
    global silent, _display, _shell

    # run setup function if running in silent mode
    if silent:
        setup(_display, _shell, silent=True)
        return
    # prompt user for confirmation otherwise
    answer = input(f"Do you want to setup {name}? (y/n [n]) ")
    if answer and answer.lower()[0] == "y":
        setup(_display, _shell)


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
