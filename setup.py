#!/usr/bin/env python3

import scripts.lib.display as display
import scripts.git as git
import scripts.homebrew as homebrew
import scripts.macos as macos
import scripts.python as python
import scripts.zsh as zsh

verbose: bool = False
"""Print verbose messages."""
debug: bool = False
"""Print debug messages."""


def main():
    # set display mode
    display.debug_mode = debug
    display.verbose_mode = verbose
    # print setup display mode
    if debug:
        display.debug("Debug mode is enabled.")
    if verbose:
        display.verbose("Verbose mode is enabled.")
    # print setup header
    display.header("Setting up machine...")

    # setup components
    homebrew.setup()
    git.setup()
    zsh.setup()
    python.setup()
    macos.setup()

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
    args = parser.parse_args()

    # assign arguments to global variables
    verbose = args.verbose
    debug = args.debug

    # run main function
    main()
