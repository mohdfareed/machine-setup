"""Setup module containing a `setup` function for setting up Git on a new
machine."""

import logging
import os

import config
import utils
from scripts.package_managers import APT, HomeBrew, WinGet

LOGGER = logging.getLogger(__name__)
"""The git setup logger."""


def setup(
    pkg_manager: HomeBrew | APT | WinGet,
    gitconfig=config.gitconfig,
    gitignore=config.gitignore,
) -> None:
    """Setup git on a new machine."""
    LOGGER.info("Setting up git...")
    if not os.path.exists(gitconfig):
        raise utils.SetupError("Machine gitconfig file does not exist.")
    if not os.path.exists(gitignore):
        raise utils.SetupError("Machine gitignore file does not exist.")

    # install git
    if isinstance(pkg_manager, HomeBrew):
        pkg_manager.install("git git-lfs")
    if isinstance(pkg_manager, APT):
        pkg_manager.install("git git-lfs")
    if isinstance(pkg_manager, WinGet):
        pkg_manager.install(
            "Git.Git GitHub.GitLFS GitHub.CLI "
            "Microsoft.GitCredentialManagerCore"
        )

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
    raise RuntimeError("This script is not meant to be run directly.")
