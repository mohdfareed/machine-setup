#!/usr/bin/env python3

import logging

import scripts.macos
import utils

LOGGER = logging.getLogger(__name__)
"""Main setup logger."""


def main(debug=False) -> None:
    """Setup the machine.

    Args:
        debug (bool): Whether to log debug messages.
    """
    utils.setup_logging(debug)

    LOGGER.info("Setting up machine...")
    scripts.run_setup(scripts.macos.setup)
    LOGGER.warning("Restart for some changes to apply.")
    LOGGER.info("Machine setup complete.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Setup machine.")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="print debug messages"
    )

    args = parser.parse_args()
    main(args.debug)
