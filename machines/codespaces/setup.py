"""Setup module containing a `setup` function for setting up a codespace."""

import logging

import utils
from scripts.git import setup as git_setup
from scripts.shell import ZSHENV, ZSHRC
from scripts.shell import setup as shell_setup

from . import zshenv, zshrc

LOGGER = logging.getLogger(__name__)
"""The macOS setup logger."""


def setup() -> None:
    """Setup a new GitHub codespace."""
    LOGGER.info("Setting up codespace...")

    # setup core machine
    git_setup()
    shell_setup()

    # shell configuration
    utils.symlink(zshrc, ZSHRC)
    utils.symlink(zshenv, ZSHENV)

    LOGGER.info("Codespace setup complete.")


if __name__ == "__main__":
    args = utils.startup(description="Codespaces setup script.")
    utils.execute(setup)
