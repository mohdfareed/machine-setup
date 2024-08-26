"""Machine configuration files."""

import os as _os

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
