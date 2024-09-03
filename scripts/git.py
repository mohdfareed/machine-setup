"""Setup module containing a `setup` function for setting up Git on a new
machine."""

import logging
import os

import config
import utils

LOGGER = logging.getLogger(__name__)
"""The git setup logger."""


def setup() -> None:
    """Setup git on a new machine."""
    LOGGER.info("Setting up git...")

    # resolve git configuration paths
    if utils.is_windows():
        gitconfig = os.path.join(os.environ["USERPROFILE"], ".gitconfig")
        gitignore = os.path.join(os.environ["USERPROFILE"], ".gitignore")
    elif utils.is_unix():
        gitconfig = os.path.join(config.xdg_config, "git", "config")
        gitignore = os.path.join(config.xdg_config, "git", "ignore")
    else:
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")

    utils.symlink(config.gitconfig, gitconfig)
    utils.symlink(config.gitignore, gitignore)
    LOGGER.debug("Git was setup successfully.")


if __name__ == "__main__":
    args = utils.startup(description="Git setup script.")
    utils.execute(setup, args.xdg_config)
