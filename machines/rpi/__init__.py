"""Raspberry Pi specific setup module."""

import os as _os

config = _os.path.join(_os.path.dirname(_os.path.realpath(__file__)), "config")
"""The path of rpi configuration files."""

ssh_config = _os.path.join(config, "ssh.config")
"""The path of the global ssh config file."""

zshenv = _os.path.join(config, "zshenv")
"""The path of rpi zshenv file."""

zshrc = _os.path.join(config, "zshrc")
"""The path of rpi zshrc file."""
