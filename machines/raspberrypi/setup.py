"""Setup module containing a `setup` function for setting up macOS."""

import logging

import config
import utils
from scripts.brew import setup as brew_setup
from scripts.git import setup as git_setup
from scripts.shell import ZSHENV, ZSHRC
from scripts.shell import setup as shell_setup
from scripts.ssh import setup as ssh_setup

from . import zshenv, zshrc

VSCODE = "~/Library/Application Support/Code/User"
"""The path to the VSCode user settings directory on macOS."""
LOGGER = logging.getLogger(__name__)
"""The Raspberry Pi setup logger."""


def setup() -> None:
    """Setup Raspberry Pi on a new machine."""
    LOGGER.info("Setting up Raspberry Pi...")

    # setup core machine
    git_setup()
    brew_setup()
    shell_setup()
    ssh_setup()

    # shell configuration
    utils.symlink(zshrc, ZSHRC)
    utils.symlink(zshenv, ZSHENV)

    # setup vscode settings
    LOGGER.debug("Setting up VSCode...")
    utils.symlink_at(config.vscode_settings, VSCODE)
    utils.symlink_at(config.vscode_keybindings, VSCODE)
    utils.symlink_at(config.vscode_snippets, VSCODE)

    LOGGER.info("Raspberry Pi setup complete.")
    LOGGER.warning("Restart for some changes to apply.")


if __name__ == "__main__":
    args = utils.startup(description="Raspberry Pi setup script.")
    utils.execute(setup)
