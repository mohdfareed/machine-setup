"""Setup module containing a `setup` function for setting up VSCode on a new machine."""

__all__ = ["setup", "setup_tunnels"]

import logging
import os
from typing import Union

import config
import utils
from scripts.package_managers import HomeBrew, SnapStore, WinGet
from utils import shell

LOGGER = logging.getLogger(__name__)
"""The VSCode setup logger."""

vscode: str
"""The path to the VSCode user settings directory."""

if utils.is_macos():
    vscode = os.path.join(
        os.path.expanduser("~"),
        "Library",
        "Application Support",
        "Code",
        "User",
    )
elif utils.is_linux():
    vscode = os.path.join(os.path.expanduser("~"), ".config", "Code", "User")
else:  # windows
    vscode = os.path.join(os.environ["APPDATA"], "Code", "User")


def setup(pkg_manager: Union[HomeBrew, SnapStore, WinGet]) -> None:
    """Setup VSCode on a new machine."""
    LOGGER.info("Setting up VSCode...")
    install(pkg_manager)
    for file in os.listdir(config.vscode):
        utils.symlink_at(os.path.join(config.vscode, file), vscode)
    LOGGER.debug("VSCode was setup successfully.")


def install(pkg_manager: Union[HomeBrew, SnapStore, WinGet]) -> None:
    if isinstance(pkg_manager, HomeBrew) and (brew := pkg_manager):
        brew.install("visual-studio-code")
    if isinstance(pkg_manager, WinGet) and (winget := pkg_manager):
        winget.install("Microsoft.VisualStudioCode")
    if isinstance(pkg_manager, SnapStore) and (snap := pkg_manager):
        snap.install("code", classic=True)


def setup_tunnels(name: str) -> None:
    """Setup VSCode SSH tunnels as a service."""
    if not utils.is_installed("code"):
        raise utils.SetupError("VSCode is not installed on this machine.")

    LOGGER.info("Setting up VSCode SSH tunnels...")
    cmd = f"code tunnel service install " f"--accept-server-license-terms --name {name}"
    shell.run(cmd, info=True)
    LOGGER.debug("VSCode SSH tunnels were setup successfully.")
