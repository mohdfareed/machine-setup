"""Setup module containing a `setup` function for setting up Git on a new
machine."""

import logging
import os

import config
import scripts
import utils

LOGGER = logging.getLogger(__name__)
"""The git setup logger."""


def setup() -> None:
    """Setup git on a new machine."""
    LOGGER.info("Setting up git...")

    # install git
    if not (
        scripts.brew.try_install("git git-lfs")
        or scripts.apt.try_install("git git-lfs")
        or scripts.winget.try_install(
            "Git.Git GitHub.GitLFS GitHub.CLI "
            "Microsoft.GitCredentialManagerCore"
        )
    ):
        LOGGER.error("Could not install git. Please install it manually.")

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
    utils.execute(setup)
