"""Setup module containing a `setup` function for setting up a codespace."""

import logging

import utils
from machines import codespaces
from scripts import git, shell

LOGGER = logging.getLogger(__name__)
"""The codespaces setup logger."""


def setup() -> None:
    """Setup a new GitHub codespace."""
    LOGGER.info("Setting up codespace...")

    git.setup()
    shell.setup(zshrc=codespaces.zshrc)

    LOGGER.info("Codespace setup complete.")


if __name__ == "__main__":
    args = utils.startup(description="Codespaces setup script.")
    utils.execute(setup)
