"""Setup module containing a `setup` function for setting up Git on a new
machine."""

import logging
import os

import config
import utils

GITCONFIG: str = os.path.abspath("~/.gitconfig")
"""The path to the git configuration file on the machine."""
GITIGNORE: str = os.path.abspath("~/.gitignore")
"""The path to the git ignore file on the machine."""

LOGGER = logging.getLogger(__name__)
"""The git setup logger."""


def setup() -> None:
    """Setup git on a new machine."""
    LOGGER.info("Setting up git...")

    # symlink configuration file
    utils.symlink(config.gitconfig, GITCONFIG)
    utils.symlink(config.gitignore, GITIGNORE)

    LOGGER.info("Git was setup successfully.")


if __name__ == "__main__":
    import argparse

    import scripts

    parser = argparse.ArgumentParser(description="Git setup script.")
    args = parser.parse_args()
    scripts.run_setup(setup)
