"""Raspberry Pi specific setup module."""

import os as _os

config = _os.path.join(_os.path.dirname(_os.path.realpath(__file__)), "config")
"""The path of rpi configuration files."""

packages = _os.path.join(config, "packages.sh")
"""The path of rpi specific packages file."""

zshenv = _os.path.join(config, "zshenv")
"""The path of rpi zshenv file."""

zshrc = _os.path.join(config, "zshrc")
"""The path of rpi zshrc file."""
