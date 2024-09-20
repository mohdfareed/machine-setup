"""Gleason specific setup module."""

import os as _os

from . import wsl  # type: ignore

config = _os.path.join(_os.path.dirname(_os.path.realpath(__file__)))
gitconfig = _os.path.join(config, ".gitconfig")
