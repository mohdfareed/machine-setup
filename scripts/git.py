"""Setup module containing a `setup` function for setting up Git on a new
machine."""

import logging
import os

import config
import utils
from utils import shell

LOGGER = logging.getLogger(__name__)
"""The git setup logger."""


def setup(xdg_config: str | None = None) -> None:
    """Setup git on a new machine."""
    LOGGER.info("Setting up git...")

    if xdg_config is None:
        xdg_config = shell.run("echo $XDG_CONFIG_HOME")[1]
    if not xdg_config:
        xdg_config = os.path.expanduser("~/.config")

    # resolve git configuration paths
    gitconfig = os.path.join(xdg_config, "git", "config")
    gitignore = os.path.join(xdg_config, "git", "ignore")

    utils.symlink(config.gitconfig, gitconfig)
    utils.symlink(config.gitignore, gitignore)
    LOGGER.debug("Git was setup successfully.")


if __name__ == "__main__":
    args = utils.startup(description="Git setup script.")
    utils.execute(setup)
