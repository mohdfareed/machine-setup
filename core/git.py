"""Setup module containing a `setup` function for setting up Git on a new
machine."""

import logging
import os

import config
from utils.shell import Shell

GITCONFIG: str = os.path.abspath("~/.gitconfig")
"""The path to the git configuration file on the machine."""
GITIGNORE: str = os.path.abspath("~/.gitignore")
"""The path to the git ignore file on the machine."""

LOGGER = logging.getLogger(__name__)
"""The git setup logger."""
shell = Shell(LOGGER.debug, LOGGER.error)
"""The git shell instance."""


def setup() -> None:
    """Setup git on a new machine."""
    LOGGER.info("Setting up git...")

    # symlink configuration file
    os.makedirs(os.path.dirname(GITCONFIG), exist_ok=True)
    os.remove(GITCONFIG)
    os.symlink(config.gitconfig, GITCONFIG)
    os.makedirs(os.path.dirname(GITIGNORE), exist_ok=True)
    os.remove(GITIGNORE)
    os.symlink(config.gitignore, GITIGNORE)

    LOGGER.info("Git was setup successfully.")


if __name__ == "__main__":
    import argparse

    import core

    parser = argparse.ArgumentParser(description="Git setup script.")
    args = parser.parse_args()
    core.run(setup, LOGGER, "Failed to setup git")
