"""Setup module containing a `setup` function for setting up Vim on a new machine."""

__all__ = ["setup"]

import logging
import os
from typing import Union

import config
import core
import utils
from scripts.package_managers import APT, HomeBrew, WinGet

LOGGER = logging.getLogger(__name__)
"""The git setup logger."""


def setup(
    pkg_manager: Union[HomeBrew, APT, WinGet],
    gitconfig: str = config.gitconfig,
    gitignore: str = config.gitignore,
) -> None:
    """Setup git on a new machine."""
    LOGGER.info("Setting up git...")
    _install(pkg_manager)

    if not os.path.exists(gitconfig):
        raise core.SetupError("Machine gitconfig file does not exist.")
    if not os.path.exists(gitignore):
        raise core.SetupError("Machine gitignore file does not exist.")

    if config.xdg_config:  # resolve git configuration paths
        gitconfig_path = os.path.join(config.xdg_config, "git", "config")
        gitignore_path = os.path.join(config.xdg_config, "git", "ignore")
    elif utils.is_windows():
        gitconfig_path = os.path.join(os.environ["USERPROFILE"], ".gitconfig")
        gitignore_path = os.path.join(os.environ["USERPROFILE"], ".gitignore")
    else:
        raise utils.Unsupported(f"Unsupported operating system: {utils.OS}")

    utils.symlink(gitconfig, gitconfig_path)
    utils.symlink(gitignore, gitignore_path)
    LOGGER.debug("Git was setup successfully.")


def _install(pkg_manager: Union[HomeBrew, APT, WinGet]) -> None:
    if isinstance(pkg_manager, HomeBrew):
        pkg_manager.install("git git-lfs gh")
    if isinstance(pkg_manager, APT):
        pkg_manager.install("git git-lfs")
        pkg_manager.add_keyring(
            "https://cli.github.com/packages/githubcli-archive-keyring.gpg",
            "https://cli.github.com/packages stable main",
            "github-cli",
        )
        pkg_manager.install("gh")
    if isinstance(pkg_manager, WinGet):
        pkg_manager.install("Git.Git GitHub.GitLFS GitHub.CLI Microsoft.GitCredentialManagerCore")
