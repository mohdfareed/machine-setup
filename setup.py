#!/usr/bin/env python3

import os

import config
import core
import utils

printer = utils.Printer("setup")
"""The main setup printer."""


def main(config_path: str | None, log=False, debug=False) -> None:
    """Setup the machine.

    Args:
        config_path (str): Path to the local config directory.
        log (bool): Whether to log output to a file.
        debug (bool): Whether to log debug messages.
    """

    # initial setup
    os.chdir(os.path.dirname(utils.abspath(__file__)))
    utils.Printer.initialize(to_file=log, debug=debug)
    printer.debug("Debug mode enabled") if debug else None
    initial_setup(config_path) if config_path else None

    try:  # setup the machine
        setup_machine(config_path)
    except Exception as exception:
        # printer.logger.exception(exception) if printer.debug_mode else None
        printer.error("Failed to setup machine.")
        exit(1)
    printer.success("Machine setup complete")


def initial_setup(config_path: str) -> None:
    """initial setup of the machine."""
    printer.info("Performing initial setup...")

    # symlink profile files
    config_path = utils.abspath(config_path)
    utils.symlink(utils.abspath(config_path, "machine.sh"), config.zprofile)
    utils.symlink(utils.abspath(config_path, "pi.sh"), config.pi_zprofile)


def setup_machine(config_path: str | None) -> None:
    """Run the setup scripts."""
    printer.info("Setting up machine...\n")
    keys_dir = utils.abspath(config_path, "keys") if config_path else None

    # run setup scripts
    core.brew.setup()
    print()
    core.shell.setup()
    print()
    core.ssh.setup(keys_dir)
    print()
    core.git.setup()
    print()
    # python.setup()
    # print()
    # macos.setup()
    # print()
    # print()
    core.raspberrypi.setup()
    print()

    printer.info("Restart for some changes to apply")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Setup machine.")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="start in debug mode"
    )
    parser.add_argument(
        "-l", "--log", action="store_true", help="log to a file"
    )
    parser.add_argument(
        "config_path", nargs="?", type=str, help="local machine config path"
    )

    args = parser.parse_args()
    main(args.config_path, args.log, args.debug)
