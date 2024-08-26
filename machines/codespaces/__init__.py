"""macOS specific setup module."""

import os as _os

import utils as _utils

# macos
codespaces = _os.path.dirname(_os.path.realpath(__file__))
"""The path of codespaces configuration files."""
zshenv = _os.path.join(codespaces, "zshenv")
"""The path of codespaces zshenv file."""
zshrc = _os.path.join(codespaces, "zshrc")
"""The path of codespaces zshrc file."""

# xdg directories
xdg_config = _utils.load_env_var(zshenv, "XDG_CONFIG_HOME")
"""The path of the XDG configuration directory."""
zdotdir = _utils.load_env_var(zshenv, "ZDOTDIR")
"""The path of the ZDOTDIR directory."""
