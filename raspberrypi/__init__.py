"""Raspberry Pi specific setup module."""

import os as _os

import utils as _utils

# rpi
rpi = _os.path.join(_os.path.dirname(_os.path.realpath(__file__)), "config")
"""The path of rpi configuration files."""
zshenv = _os.path.join(rpi, "zshenv")
"""The path of rpi zshenv file."""
zshrc = _os.path.join(rpi, "zshrc")
"""The path of rpi zshrc file."""

# private files
private_machine = _utils.load_env_var(zshenv, "PRIVATE_MACHINE")
"""The path of the machine private files directory."""
private_env = _os.path.join(private_machine, "env.sh")
"""The path of the machine private environment file."""
ssh_keys = _os.path.join(private_machine, "keys")
"""The path of the machine ssh keys directory."""

# xdg directories
xdg_config = _utils.load_env_var(zshenv, "XDG_CONFIG_HOME")
"""The path of the XDG configuration directory."""
zdotdir = _utils.load_env_var(zshenv, "ZDOTDIR")
"""The path of the ZDOTDIR directory."""
