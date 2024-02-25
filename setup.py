#!/usr/bin/env python3

import logging
import os
from typing import Optional

import config
import core.brew
import core.git
import core.macos
import core.python
import core.raspberrypi
import core.shell
import core.ssh
import utils

LOGGER = logging.getLogger(__name__)
"""Main setup logger."""


def main(debug=False) -> None:
    """Setup the machine.

    Args:
        debug (bool): Whether to log debug messages.
    """
    config_path = os.getcwd()  # path to the machine configuration
    machine_path = os.path.dirname(os.path.realpath(__file__))

    # initial setup
    os.chdir(machine_path)
    utils.setup_logging(debug)
    keys_path = initial_setup(config_path)

    try:  # setup the machine
        setup_machine(keys_path)
    except KeyboardInterrupt:
        LOGGER.warning("Setup interrupted.")
        exit(0)
    except Exception as exception:
        LOGGER.exception(exception)
        LOGGER.error("Failed to setup machine.")
        exit(1)
    LOGGER.info("Machine setup complete.")


def initial_setup(config_path: str):
    """initial setup of the machine."""
    LOGGER.info("Performing initial setup...")

    # symlink profile files
    config_path = os.path.abspath(config_path)
    os.remove(config.zprofile)
    os.symlink(os.path.join(config_path, "machine.sh"), config.zprofile)
    os.remove(config.pi_zprofile)
    os.symlink(os.path.join(config_path, "pi.sh"), config.pi_zprofile)

    # return ssh keys path
    return os.path.join(config_path, "keys")


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
    LOGGER.info("Restart for some changes to apply")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Setup machine.")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="log debug messages"
    )

    args = parser.parse_args()
    main(args.debug)
