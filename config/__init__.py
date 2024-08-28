"""Machine configuration files."""

import os as _os

import utils as _utils

config = _os.path.dirname(_os.path.realpath(__file__))
"""The path to the machine configuration directory."""

vim = _os.path.join(config, "vim")
"""The path of vim configuration files."""

vscode = _os.path.join(config, "vscode")
"""The path of VSCode configuration directory."""

gitconfig = _os.path.join(config, ".gitconfig")
"""The path of the global gitconfig file."""
gitignore = _os.path.join(config, ".gitignore")
"""The path of the global gitignore file."""

brewfile = _os.path.join(config, "brewfile")
"""The path of Homebrew packages file."""

ps_profile = _os.path.join(config, "powershell.ps1")
"""The path of the PowerShell profile file."""

ssh_config = _os.path.join(config, "ssh.config")
"""The path of the global ssh config file."""

tmux = _os.path.join(config, "tmux.conf")
"""The path of the tmux configuration file."""

zshrc = _os.path.join(config, "zshrc")
"""The path of zshrc file."""
zshenv = _os.path.join(config, "zshenv")
"""The path of zshenv file."""

# environment variables

MACHINE = _utils.load_env_var(zshenv, "MACHINE")
"""The path to the machine repository."""

xdg_config = _utils.load_env_var(zshenv, "XDG_CONFIG_HOME")
"""The path of the XDG configuration directory."""

zdotdir = _utils.load_env_var(zshenv, "ZDOTDIR")
"""The path of the ZDOTDIR directory."""

private_env = _utils.load_env_var(zshenv, "PRIVATE_ENV")
"""The path of the machine private environment file."""

ssh_keys = _utils.load_env_var(zshenv, "SSH_KEYS")
"""The path of the machine ssh keys directory."""
