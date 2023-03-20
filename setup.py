#!/usr/bin/env python3

from setup_modules import *
from utils import Display

no_logging: bool = True
"""Do not log output to a file."""
verbose: bool = False
"""Print verbose output."""
debug: bool = False
"""Print debug output."""


def main():
    # set display mode
    display = Display(verbose_mode=verbose,
                      debug_mode=debug,
                      no_logging=no_logging)
    # print setup display mode
    if debug:
        display.debug("Debug mode is enabled.")
    if verbose:
        display.verbose("Verbose mode is enabled.")

    # print setup header
    # ask user if they want to run specific scripts
    display.header("Setting up machine...")

    # setup components
    setup_homebrew(display)
    # git.setup()
    # zsh.setup()
    # python.setup()
    # macos.setup()

    # inform user that setup is complete and a restart is required
    display.print("")
    display.success("Machine setup complete!")
    display.info("Please restart your machine for some changes to apply.")


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
