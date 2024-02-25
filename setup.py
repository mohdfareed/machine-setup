#!/usr/bin/env python3

import os
from typing import Optional

import config
import core
import utils

printer = utils.Printer("setup")
"""The main setup printer."""


def main(log=True, debug=False) -> None:
    """Setup the machine.

    Args:
        log (bool): Whether to log output to a file.
        debug (bool): Whether to log debug messages.
    """

    # initial setup
    config_path = os.getcwd()
    os.chdir(os.path.dirname(utils.abspath(__file__)))
    utils.Printer.initialize(to_file=log, debug=debug)
    keys = initial_setup(config_path)

    try:  # setup the machine
        setup_machine(keys)
    except KeyboardInterrupt:
        printer.error("Setup interrupted")
        exit(0)
    except Exception as exception:
        printer.logger.exception(exception) if printer.debug_mode else None
        printer.error("Failed to setup machine.")
        exit(1)
    printer.success("Machine setup complete")


def initial_setup(config_path: str):
    """initial setup of the machine."""
    printer.info("Performing initial setup...")

    # symlink profile files
    config_path = utils.abspath(config_path)
    utils.symlink(utils.abspath(config_path, "machine.sh"), config.zprofile)
    utils.symlink(utils.abspath(config_path, "pi.sh"), config.pi_zprofile)
    # return ssh keys path
    return utils.abspath(config_path, "keys")


def setup_machine(keys: Optional[str]) -> None:
    """Run the setup scripts."""

    print()
    core.brew.setup()
    print()
    core.shell.setup()
    print()
    core.ssh.setup(keys)
    print()
    core.git.setup()
    print()
    core.python.setup()
    print()
    core.macos.setup()
    print()
    core.raspberrypi.setup()
    print()

    printer.info("Restart for some changes to apply")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Setup machine.")
    parser.add_argument(
        "-l", "--log", action="store_false", help="log output to a file"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="log debug messages"
    )

    args = parser.parse_args()
    main(args.log, args.debug)
