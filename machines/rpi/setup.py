"""Setup module containing a `setup` function for setting up macOS."""

import logging

import utils
from machines import rpi
from scripts import brew, git, shell, ssh, vscode

VSCODE = "~/Library/Application Support/Code/User"
"""The path to the VSCode user settings directory on macOS."""
LOGGER = logging.getLogger(__name__)
"""The Raspberry Pi setup logger."""


def setup() -> None:
    """Setup Raspberry Pi on a new machine."""
    LOGGER.info("Setting up Raspberry Pi...")

    # setup core machine
    git.setup()
    brew.setup()
    shell.setup(rpi.xdg_config, rpi.zdotdir, rpi.zshrc, rpi.zshenv)
    ssh.setup(rpi.ssh_keys)
    vscode.setup()

    LOGGER.info("Raspberry Pi setup complete.")
    LOGGER.warning("Restart for some changes to apply.")


if __name__ == "__main__":
    args = utils.startup(description="Raspberry Pi setup script.")
    utils.execute(setup)
