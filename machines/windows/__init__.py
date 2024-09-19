"""Windows specific setup module."""

import os
from typing import Callable

import utils
from machines import LOGGER

config = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config")
"""The path of macOS configuration files."""

ps_profile = os.path.join(config, "ps_profile.ps1")
"""The path of Windows Powershell profile file."""

ssh_config = os.path.join(config, "ssh.config")
"""The path of the global ssh config file."""


# FIXME: find better way to run wsl setup script, doesn't work as is
def setup_wsl(wsl_setup_handler: Callable[[], None]) -> None:
    """Setup WSL on a new machine."""
    LOGGER.info("Setting up WSL...")
    utils.shell.run("wsl --install", info=True)
    current_shell = utils.shell.EXECUTABLE

    utils.shell.EXECUTABLE = utils.shell.SupportedExecutables.WSL
    wsl_setup_handler()
    utils.shell.EXECUTABLE = current_shell
    LOGGER.info("WSL setup complete.")


__all__ = ["config", "ps_profile", "ssh_config", "setup_wsl"]
