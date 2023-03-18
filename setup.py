#!/usr/bin/env python3

import scripts.homebrew as homebrew
import scripts.git as git
import scripts.zsh as zsh
import scripts.python as python
import scripts.macos as macos
from scripts.lib import display

verbose: bool = False
"""Print verbose messages."""
debug: bool = False
"""Print debug messages."""


def main():
    # set display mode
    display.verbose_mode = verbose
    display.debug_mode = debug
    # setup components
    homebrew.setup()
    git.setup()
    zsh.setup()
    python.setup()
    macos.setup()


if __name__ == "__main__":
    import argparse
    # parse command line arguments
    parser = argparse.ArgumentParser(description="Machine setup script.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print verbose messages")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="print debug messages",)
    args = parser.parse_args()
    # assign arguments to global variables
    verbose = args.verbose
    debug = args.debug
    # run main function
    main()
