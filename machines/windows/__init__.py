"""Windows specific setup module."""

import os as _os
import sys as _sys
from types import ModuleType as _ModuleType

import utils as _utils
from machines import LOGGER as _LOGGER

from . import wsl  # type: ignore

config = _os.path.join(_os.path.dirname(_os.path.realpath(__file__)), "config")
ps_profile = _os.path.join(config, "ps_profile.ps1")
ssh_config = _os.path.join(config, "ssh.config")


def setup_wsl(wsl_module: _ModuleType, setup_args: str = "") -> None:
    """Setup WSL on a new machine."""

    _LOGGER.info("Setting up WSL...")
    _utils.shell.run("wsl --install", info=True)
    current_shell = _utils.shell.EXECUTABLE
    _utils.shell.EXECUTABLE = _utils.shell.SupportedExecutables.WSL
    _utils.shell.run(f"{_sys.executable} {wsl_module.__name__} {setup_args}")
    _utils.shell.EXECUTABLE = current_shell
    _LOGGER.info("WSL setup complete.")
