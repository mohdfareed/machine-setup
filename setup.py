#!/usr/bin/env python3

from setup_modules import *
from utils import Display
from utils import Shell
from typing import Callable

no_logging: bool = True
"""Do not log output to a file."""
verbose: bool = True
"""Print verbose output."""
debug: bool = True
"""Print debug output."""


def main():
    """Run the main function of the setup script. This function is called when
    the script is run from the command line. It will prompt the user to run
    a setup function for every setup module. By default, the setup is run in
    verbose and debug mode without logging output to a file."""

    # create a shell instance and set display mode
    display = Display(verbose, debug, no_logging)
    shell = Shell()

    # print setup display mode
    if debug:
        display.debug("Debug mode is enabled.")
    if verbose:
        display.verbose("Verbose mode is enabled.")
    # print setup header
    display.header("Setting up machine...")

    # resources repo and path
    repo = "git@github.com:mohdfareed/setup-resources.git"
    resources = "resources"
    # print resources path for debugging
    display.debug(f"resources: {resources}")
    # clone resources repo
    shell.run_quiet(f"git clone --recurse-submodules {repo} {resources}",
                    display.verbose, display.print,
                    "Cloning resources repository")

    # prompt user to setup components
    _prompt_setup(setup_homebrew, "Homebrew", display)
    _prompt_setup(setup_git, "Git", display)
    _prompt_setup(setup_zsh, "Zsh", display)
    _prompt_setup(setup_python, "Python", display)
    _prompt_setup(setup_macos, "macOS", display)

    # inform user that setup is complete and a restart is required
    print("")  # leave a blank line
    display.success("Machine setup complete!")
    display.info("Please restart your machine for some changes to apply.")


def _prompt_setup(setup_function: Callable, name: str, display: Display):
    """Prompt the user to run a setup function with a `Display` object.

    Args:
        setup_function (function): The setup function to run.
        display (Display): The display for printing output.
    """
    answer = input(f"Do you want to setup {name}? (y/n [n]) ")
    if answer and answer.lower()[0] == "y":
        setup_function(display)


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
