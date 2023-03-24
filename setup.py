#!/usr/bin/env python3

from setup_modules import homebrew, git, zsh, python, macos
from utils.display import Display
from utils.shell import Shell
from typing import Callable
import os

# TODO: add an unattended mode that does not prompt the user to run setup

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
        return
    # get resources if not already present
    if shell.run_quiet("git submodule init && git submodule update --remote",
                       display.verbose, "Initializing resources") != 0:
        display.error("Failed to initialize resources.")
        return

    # prompt user to setup components
    _prompt_setup(homebrew.setup, "Homebrew", display)
    _prompt_setup(git.setup, "Git", display)
    _prompt_setup(zsh.setup, "Zsh", display)
    _prompt_setup(python.setup, "Python", display)
    _prompt_setup(macos.setup, "macOS", display)

    # inform user that setup is complete and a restart is required
    display.success("\nMachine setup complete!")
    display.info("Please restart your machine for some changes to apply.")


def _init() -> tuple[Display, Shell]:
    """Setup objects for the setup script. It sets the working directory,
    creates a `Display` and `Shell` object, and prints the setup display mode.

    Returns:
        tuple[Display, Shell]: A list containing the `Display` and `Shell`.
    """

    # create a shell instance and set display mode
    display = Display(verbose, debug, no_logging)
    shell = Shell()
    # print setup display mode
    display.debug("Debug mode is enabled.") if debug else None
    display.verbose("Verbose mode is enabled.") if verbose else None

    return display, shell


def _prompt_setup(function: Callable, name: str, display: Display) -> None:
    """Prompt the user to run a setup function with a `Display` object. It will
    run the function if the user enters "y" or "yes". The function should take
    a `Display` object as its only argument.

    Args:
        function (function): The setup function to run.
        display (Display): The display for printing output.
    """
    answer = input(f"Do you want to setup {name}? (y/n [n]) ")
    if answer and answer.lower()[0] == "y":
        function(display)


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
    args = parser.parse_args()

    # assign arguments to global variables
    verbose = args.verbose
    debug = args.debug
    no_logging = args.no_log

    # run main function
    main()
