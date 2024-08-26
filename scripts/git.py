"""Setup module containing a `setup` function for setting up Git on a new
machine."""

import logging
import os

import config
import machines.macos
import utils

GITCONFIG: str = os.path.join(machines.macos.xdg_config, "git", "config")
"""The path to the git configuration file on the machine."""
GITIGNORE: str = os.path.join(machines.macos.xdg_config, "git", "ignore")
"""The path to the git ignore file on the machine."""

LOGGER = logging.getLogger(__name__)
"""The git setup logger."""


def setup() -> None:
    """Setup git on a new machine."""
    LOGGER.info("Setting up git...")
    utils.symlink(config.gitconfig, GITCONFIG)
    utils.symlink(config.gitignore, GITIGNORE)
    LOGGER.info("Git was setup successfully.")


if __name__ == "__main__":
    utils.parser.description = "Git setup script."
    args = utils.startup()
    utils.execute(setup)
