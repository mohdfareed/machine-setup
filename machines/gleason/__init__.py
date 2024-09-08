"""Gleason specific setup module."""

import os as _os

config = _os.path.join(_os.path.dirname(_os.path.realpath(__file__)))
"""The path of GLeason configuration files."""
gitconfig = _os.path.join(config, ".gitconfig")
"""The path of Gleason's git configuration file."""
