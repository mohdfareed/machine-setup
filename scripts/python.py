"""Setup module containing a `setup` function for setting up Python on a new
machine."""

import logging
import os

import config
import utils
from scripts.brew import BIN

LOGGER = logging.getLogger(__name__)
"""The Python setup logger."""
PIP = os.path.join(BIN, "pip")
"""The path to the pip executable."""


def setup() -> None:
    """Setup Python on a new machine. Homebrew's Python is used."""
    LOGGER.info("Setting up Python...")

    # check if python is installed
    if not os.path.exists(PIP):
        LOGGER.info("Python is not installed")
        return

    # install global python packages
    LOGGER.info("Installing Python requirements...")
    cmd = [PIP, "install", "--upgrade", "pip"]
    utils.run_cmd(cmd, msg="Upgrading pip")
    cmd = [PIP, "install", "-r", config.requirements, "--upgrade"]
    utils.run_cmd(cmd, msg="Installing")

    # cleanup
    utils.run_cmd([PIP, "cache", "purge"], msg="Cleaning up")
    LOGGER.info("Python setup complete")


if __name__ == "__main__":
    import argparse

    import scripts

    parser = argparse.ArgumentParser(description="Python setup script.")
    args = parser.parse_args()
    scripts.run_setup_isolated(setup)
