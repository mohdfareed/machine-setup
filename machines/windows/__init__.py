"""Windows specific setup module."""

import os as _os
from typing import Callable as _Callable

import utils as _utils
from machines import LOGGER

config = _os.path.join(_os.path.dirname(_os.path.realpath(__file__)), "config")
"""The path of macOS configuration files."""

ps_profile = _os.path.join(config, "ps_profile.ps1")
"""The path of Windows Powershell profile file."""

ssh_config = _os.path.join(config, "ssh.config")
"""The path of the global ssh config file."""


# FIXME: find better way to run wsl setup script, doesn't work as is
def setup_wsl(wsl_setup_handler: _Callable) -> None:
    """Setup WSL on a new machine."""
    LOGGER.info("Setting up WSL...")
    _utils.shell.run("wsl --install", info=True)
    current_shell = _utils.shell.EXECUTABLE

    _utils.shell.EXECUTABLE = _utils.shell.SupportedExecutables.WSL
    wsl_setup_handler()
    _utils.shell.EXECUTABLE = current_shell
    LOGGER.info("WSL setup complete.")
