"""Codespaces specific setup module."""

__all__ = ["config", "zshrc"]

import os

config = os.path.join(os.path.dirname(os.path.realpath(__file__)))
"""The path of codespaces configuration files."""
zshrc = os.path.join(config, "zshrc")
"""The path of codespaces zshrc file."""
