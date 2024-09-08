"""Setup module containing a `setup` function for setting up Git on a new
machine."""

import logging
import os

import config
import scripts
import utils

LOGGER = logging.getLogger(__name__)
"""The git setup logger."""


def setup(gitconfig=config.gitconfig, gitignore=config.gitignore) -> None:
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
        gitconfig_path = os.path.join(os.environ["USERPROFILE"], ".gitconfig")
        gitignore_path = os.path.join(os.environ["USERPROFILE"], ".gitignore")
    elif utils.is_unix():
        gitconfig_path = os.path.join(config.xdg_config, "git", "config")
        gitignore_path = os.path.join(config.xdg_config, "git", "ignore")
    else:
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")

    utils.symlink(gitconfig, gitconfig_path)
    utils.symlink(gitignore, gitignore_path)
    LOGGER.debug("Git was setup successfully.")


if __name__ == "__main__":
    args = utils.startup(description="Git setup script.")
    utils.execute(setup)
