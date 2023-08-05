"""Setup module containing a `setup` function for setting up Python on a new
machine."""

import os

import config
import utils
from core.brew import BIN

printer = utils.Printer("python")
"""The Python setup printer."""
shell = utils.Shell(printer.debug, printer.error, printer.logger.debug)
"""The Python shell instance."""

PIP = os.path.join(BIN, "pip")
"""The path to the pip executable."""


def setup() -> None:
    """Setup Python on a new machine. Homebrew's Python is used."""
    printer.info("Setting up Python...")

    # install python requirements
    printer.print("Installing Python requirements...")
    cmd = [PIP, "install", "--upgrade", "pip"]
    shell(cmd, silent=True, status="Upgrading pip...")
    cmd = [PIP, "install", "-r", config.requirements, "--upgrade"]
    shell(cmd, silent=True, status="Installing...")

    # cleanup
    shell([PIP, "cache", "purge"], status="Cleaning up...")
    printer.success("Python setup complete")


if __name__ == "__main__":
    import argparse

    import core

    parser = argparse.ArgumentParser(description="Python setup script.")
    args = parser.parse_args()
    core.run(setup, printer, "Failed to setup Python")
