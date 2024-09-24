"""Setup module containing a `setup` function for setting up the shell on a new machine."""

__all__ = ["setup", "setup_windows"]

import logging
import os
from typing import Union

import config
import core
import utils
from scripts.package_managers import APT, HomeBrew
from utils import shell

LOGGER = logging.getLogger(__name__)
"""The ZSH setup logger."""

if utils.is_windows():
    PS_PROFILE = os.path.join(
        os.environ["USERPROFILE"],
        "Documents",
        "WindowsPowerShell",
        "profile.ps1",
    )
    """The path to the PowerShell profile file."""

else:
    ZSHENV = os.path.join(os.path.expanduser("~"), ".zshenv")
    """The path to the zsh environment file symlink."""
    ZDOTDIR = utils.load_env_var(config.zshenv, "ZDOTDIR")
    """The path of the ZDOTDIR directory on the machine."""


def setup(
    pkg_manager: Union[HomeBrew, APT],
    zshrc: str = config.zshrc,
    zshenv: str = config.zshenv,
) -> None:
    """Setup the shell environment on a machine."""

    LOGGER.info("Setting up shell...")
    if not config.xdg_config:
        raise utils.Unsupported(f"Unsupported operating system: {utils.OS}")
    if not os.path.exists(zshrc):
        raise core.SetupError("Machine zshrc file does not exist.")
    if not os.path.exists(zshenv):
        raise core.SetupError("Machine zshenv file does not exist.")
    pkg_manager.install("zsh")  # install zsh

    # resolve shell configuration paths
    _zshrc = os.path.join(ZDOTDIR, ".zshrc")
    vim = os.path.join(config.xdg_config, "nvim")
    tmux = os.path.join(config.xdg_config, "tmux", "tmux.conf")
    ps_profile = os.path.join(config.xdg_config, "powershell", "profile.ps1")

    # symlink config files
    utils.symlink(config.vim, vim)
    utils.symlink(config.tmux, tmux)
    utils.symlink(config.ps_profile, ps_profile)
    utils.symlink(zshrc, _zshrc)
    utils.symlink(zshenv, ZSHENV)

    # update zinit and its plugins
    LOGGER.info("Updating zinit and its plugins...")
    source_env = f"source {zshrc} && source {zshenv}"
    shell.execute(f"{source_env} && zinit self-update && zinit update")

    # clean up
    shell.execute("sudo rm -rf ~/.zcompdump*", throws=False)
    shell.execute("sudo rm -rf ~/.zshrc", throws=False)
    shell.execute("sudo rm -rf ~/.zsh_sessions", throws=False)
    shell.execute("sudo rm -rf ~/.zsh_history", throws=False)
    shell.execute("sudo rm -rf ~/.lesshst", throws=False)
    LOGGER.debug("Shell setup complete.")


def setup_windows(ps_profile: str = config.ps_profile) -> None:
    """Setup the shell environment on a Windows machine."""

    LOGGER.info("Setting up shell...")
    if not config.local_data:
        raise utils.Unsupported(f"Unsupported operating system: {utils.OS}")
    if not os.path.exists(ps_profile):
        raise core.SetupError("Machine powershell profile file does not exist.")

    # resolve shell configuration paths
    vim = os.path.join(config.local_data, "nvim")
    # symlink config files
    utils.symlink(config.vim, vim)
    utils.symlink(config.ps_profile, PS_PROFILE)
    LOGGER.debug("Shell setup complete.")
