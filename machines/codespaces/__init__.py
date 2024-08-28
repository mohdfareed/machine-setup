"""Codespaces specific setup module."""

import os as _os

config = _os.path.join(_os.path.dirname(_os.path.realpath(__file__)))
"""The path of codespaces configuration files."""
zshrc = _os.path.join(config, "zshrc")
"""The path of codespaces zshrc file."""
