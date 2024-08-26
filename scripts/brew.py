"""Setup module containing a `setup` function for setting up Homebrew on a new
machine."""

import logging
import os

import config
import utils
from utils import shell

BIN = "/opt/homebrew/bin"
"""The path to the Homebrew executables."""
BREW = os.path.join(BIN, "brew")
"""The path to the brew executable."""
MAS = os.path.join(BIN, "mas")
"""The path to the mas executable."""

LOGGER = logging.getLogger(__name__)
"""The Homebrew setup logger."""


def setup(machine_brewfile: str | None = None) -> None:
    """Setup Homebrew on a new machine by installing it and its packages."""
    LOGGER.info("Setting up Homebrew...")
    install_brew()

    # install brew and core packages
    LOGGER.info("Installing core packages...")
    cmd = [BREW, "bundle", f"--file={config.brewfile}"]
    shell.run(cmd, msg="Installing packages", throws=False)

    if machine_brewfile:  # install machine specific packages
        LOGGER.info("Installing machine specific packages...")
        cmd = [BREW, "bundle", f"--file={machine_brewfile}"]
        shell.run(cmd, msg="Installing packages", throws=False)

    # upgrade packages
    LOGGER.info("Upgrading packages...")
    shell.run([BREW, "upgrade"], msg="Upgrading packages", throws=False)

    # cleanup
    LOGGER.info("Cleaning up...")
    cmd = [BREW, "cleanup", "--prune=all"]
    shell.run(cmd, msg="Cleaning up", throws=False)
    LOGGER.info("Homebrew setup complete.")


def install_brew() -> None:
    """Install Homebrew on a new machine."""

    # update homebrew if it is already installed
    if os.path.exists(BREW):
        shell.run([BREW, "update"], msg="Updating brew")
        LOGGER.info("Homebrew was updated.")

    else:  # install homebrew otherwise
        LOGGER.info("Installing Homebrew...")
        cmd = '/bin/bash -c "$(curl -fsSL https://git.io/JIY6g)"'
        shell.run(cmd, msg="Installing brew")
        LOGGER.info("Homebrew installed successfully.")

    # fix “zsh compinit: insecure directories” error
    shell.run(f'chmod -R go-w "$({BREW} --prefix)/share"')
    LOGGER.info("Fixed zsh `compinit` security error.")  # REVIEW: needed?


if __name__ == "__main__":
    args = utils.startup(description="Homebrew setup script.")
    utils.execute(setup)
