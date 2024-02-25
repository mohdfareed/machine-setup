"""Setup module containing a `setup` function for setting up Python on a new
machine."""

import logging
import os

import config
from core.brew import BIN
from utils.shell import Shell

LOGGER = logging.getLogger(__name__)
"""The Python setup logger."""
shell = Shell(LOGGER.debug, LOGGER.error, LOGGER.debug)
"""The Python shell instance."""

PIP = os.path.join(BIN, "pip")
"""The path to the pip executable."""


def setup() -> None:
    """Setup Python on a new machine. Homebrew's Python is used."""
    LOGGER.info("Setting up Python...")

    # install python requirements
    LOGGER.info("Installing Python requirements...")
    cmd = [PIP, "install", "--upgrade", "pip"]
    shell(cmd, silent=True, status="Upgrading pip...")
    cmd = [PIP, "install", "-r", config.requirements, "--upgrade"]
    shell(cmd, silent=True, status="Installing...")

    # cleanup
    shell([PIP, "cache", "purge"], status="Cleaning up...")
    LOGGER.info("Python setup complete")


if __name__ == "__main__":
    import argparse

    import core

    parser = argparse.ArgumentParser(description="Python setup script.")
    args = parser.parse_args()
    core.run(setup, LOGGER, "Failed to setup Python")
