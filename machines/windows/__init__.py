"""macOS specific setup module."""

import os as _os

from .setup import setup_wsl

config = _os.path.join(_os.path.dirname(_os.path.realpath(__file__)), "config")
"""The path of macOS configuration files."""

ps_profile = _os.path.join(config, "ps_profile.ps1")
"""The path of Windows Powershell profile file."""

ssh_config = _os.path.join(config, "ssh.config")
"""The path of the global ssh config file."""
