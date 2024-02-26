#!/usr/bin/env python3

import logging

import scripts.brew
import scripts.git
import scripts.macos
import scripts.python
import scripts.shell
import scripts.ssh
import utils

LOGGER = logging.getLogger(__name__)
"""Main setup logger."""


def main(debug=False) -> None:
    """Setup the machine.

    Args:
        debug (bool): Whether to log debug messages.
    """

    utils.logging.setup_logging(debug)
    try:  # setup the machine
        LOGGER.info("Setting up machine...")
        scripts.brew.setup()
        scripts.shell.setup()
        scripts.ssh.setup()
        scripts.git.setup()
        scripts.python.setup()
        scripts.macos.setup()
        LOGGER.warning("Restart for some changes to apply.")
    except KeyboardInterrupt:
        LOGGER.warning("Setup interrupted.")
        exit(0)
    except Exception as exception:
        LOGGER.exception(exception)
        LOGGER.error("Failed to setup machine.")
        exit(1)
    LOGGER.info("Machine setup complete.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Setup machine.")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="print debug messages"
    )

    args = parser.parse_args()
    main(args.debug)
