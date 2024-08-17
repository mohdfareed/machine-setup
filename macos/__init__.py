"""macOS-specific configuration files."""

import os as _os

import utils as _utils

# macos
macos = _os.path.join(_os.path.dirname(_os.path.realpath(__file__)), "config")
"""The path of git configuration directory."""
brewfile = _os.path.join(macos, "brewfile")
"""The path of macOS specific Homebrew packages file."""
ps_profile = _os.path.join(macos, "powershell.ps1")
"""The path of the PowerShell profile file."""
preferences = _os.path.join(macos, "preferences.sh")
"""The path of macOS preferences file of shell commands."""
ssh_config = _os.path.join(macos, "ssh.config")
"""The path of the global ssh config file."""
zshenv = _os.path.join(macos, "zshenv")
"""The path of macOS zshenv file."""
zshrc = _os.path.join(macos, "zshrc")
"""The path of macOS zshrc file."""

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
