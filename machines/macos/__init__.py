"""macOS specific setup module."""

import os as _os

config = _os.path.join(_os.path.dirname(_os.path.realpath(__file__)), "config")
"""The path of macOS configuration files."""

brewfile = _os.path.join(config, "brewfile")
"""The path of macOS specific Homebrew packages file."""

preferences = _os.path.join(config, "preferences.sh")
"""The path of macOS preferences file of shell commands."""

ssh_config = _os.path.join(config, "ssh.config")
"""The path of the global ssh config file."""

zshenv = _os.path.join(config, "zshenv")
"""The path of macOS zshenv file."""

zshrc = _os.path.join(config, "zshrc")
"""The path of macOS zshrc file."""
