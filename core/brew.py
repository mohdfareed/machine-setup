"""Setup module containing a `setup` function for setting up Homebrew on a new
machine."""

import logging
import os

import config
import utils

BIN = "/opt/homebrew/bin"
"""The path to the Homebrew executables."""
BREW = os.path.join(BIN, "brew")
"""The path to the brew executable."""
LOGGER = logging.getLogger(__name__)
"""The Homebrew setup logger."""


def setup() -> None:
    """Setup Homebrew on a new machine by installing it and its packages."""

    utils.run_shell("$MACHINE/test.sh")
    return

    LOGGER.info("Setting up Homebrew...")
    install_brew()

    # install packages from Brewfile
    LOGGER.info("Installing packages from Brewfile...")
    cmd = [BREW, "bundle", f"--file={config.brewfile}"]
    utils.run_shell(cmd, msg="Installing...")
    LOGGER.debug("Installed packages from Brewfile")

    # upgrade packages
    LOGGER.info("Upgrading packages...")
    utils.run_shell([BREW, "upgrade"], msg="Upgrading...")
    LOGGER.debug("Upgraded packages")

    # upgrade mac app store packages
    LOGGER.info("Upgrading mac app store packages...")
    mas = os.path.join(BIN, "mas")
    utils.run_shell([mas, "upgrade"], msg="Upgrading...")
    LOGGER.debug("Upgraded mac app store packages")

    # cleanup
    LOGGER.info("Cleaning up...")
    cmd = [BREW, "cleanup", "--prune=all"]
    utils.run_shell(cmd, msg="Cleaning up...")
    LOGGER.info("Homebrew setup complete")


def install_brew():
    # update homebrew if it is already installed
    if os.path.exists(BREW):
        LOGGER.info("Updating Homebrew...")
        utils.run_shell([BREW, "update"], msg="Updating...")
        LOGGER.info("Homebrew was updated")
    else:  # install homebrew otherwise
        LOGGER.info("Installing Homebrew...")
        cmd = '/bin/bash -c "$(curl -fsSL https://git.io/JIY6g)"'
        utils.run_shell(cmd, msg="Installing...")
        LOGGER.info("Homebrew installed successfully")

    # fix “zsh compinit: insecure directories” error
    utils.run_shell(f'chmod -R go-w "$({BREW} --prefix)/share"')
    LOGGER.debug("Fixed zsh `compinit` security error")  # TODO: fixed?
    # add fonts tap
    utils.run_shell(f"{BREW} tap homebrew/cask-fonts")
    LOGGER.debug("Added Homebrew fonts tap")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Homebrew setup script.")
    args = parser.parse_args()

    import core

    core.run_setup(setup)
