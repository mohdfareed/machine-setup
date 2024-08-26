"""Setup module containing a `setup` function for setting up a codespace."""

import logging

import utils
from machines.codespaces import zshenv, zshrc
from scripts import git, shell
from scripts.shell import ZSHENV, ZSHRC

LOGGER = logging.getLogger(__name__)
"""The macOS setup logger."""


def setup() -> None:
    """Setup a new GitHub codespace."""
    LOGGER.info("Setting up codespace...")

    # setup core machine
    git.setup()
    shell.setup()

    # shell configuration
    utils.symlink(zshrc, ZSHRC)
    utils.symlink(zshenv, ZSHENV)

    LOGGER.info("Codespace setup complete.")


if __name__ == "__main__":
    args = utils.startup(description="Codespaces setup script.")
    utils.execute(setup)
