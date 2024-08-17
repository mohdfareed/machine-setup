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
MAS = os.path.join(BIN, "mas")
"""The path to the mas executable."""

LOGGER = logging.getLogger(__name__)
"""The Homebrew setup logger."""


def setup(brewfile=config.brewfile) -> None:
    """Setup Homebrew on a new machine by installing it and its packages."""
    LOGGER.info("Setting up Homebrew...")
    install_brew()

    # install packages from Brewfile
    LOGGER.info("Installing packages from Brewfile...")
    cmd = [BREW, "bundle", f"--file={brewfile}"]
    utils.run(cmd, msg="Installing", throws=False)
    LOGGER.debug("Installed packages from Brewfile.")

    # upgrade packages
    LOGGER.info("Upgrading packages...")
    utils.run([BREW, "upgrade"], msg="Upgrading")
    LOGGER.debug("Upgraded packages.")

    # cleanup
    LOGGER.info("Cleaning up...")
    cmd = [BREW, "cleanup", "--prune=all"]
    utils.run(cmd, msg="Cleaning up")
    LOGGER.info("Homebrew setup complete.")

    # macos specific setup
    if not utils.is_macos():
        return

    # update app store packages
    LOGGER.info("Upgrading mac app store packages...")
    utils.run([MAS, "upgrade"], msg="Upgrading")
    LOGGER.debug("Upgraded mac app store packages.")


def install_brew() -> None:
    """Install Homebrew on a new machine."""
    # update homebrew if it is already installed
    if os.path.exists(BREW):
        utils.run([BREW, "update"], msg="Updating")
        LOGGER.info("Homebrew was updated.")
    else:  # install homebrew otherwise
        LOGGER.info("Installing Homebrew...")
        cmd = '/bin/bash -c "$(curl -fsSL https://git.io/JIY6g)"'
        utils.run(cmd, msg="Installing")
        LOGGER.info("Homebrew installed successfully.")

    # fix “zsh compinit: insecure directories” error
    utils.run(f'chmod -R go-w "$({BREW} --prefix)/share"')
    LOGGER.info("Fixed zsh `compinit` security error.")  # REVIEW: needed?


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Homebrew setup script.")
    args = parser.parse_args()

    import scripts

    scripts.run_setup_isolated(setup)
