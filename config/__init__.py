"""Machine configuration files."""

import os as _os

# core configuration files
config = _os.path.dirname(_os.path.realpath(__file__))
"""The path to the machine configuration directory."""
zshrc = _os.path.join(config, "zshrc")
"""The path of zshrc file."""
zshenv = _os.path.join(config, "zshenv")
"""The path of zshenv file."""
tmux = _os.path.join(config, "tmux.conf")
"""The path of the tmux configuration file."""
vim = _os.path.join(config, "vim")
"""The path of vim configuration files."""
brewfile = _os.path.join(config, "brewfile")
"""The path of Homebrew packages file."""
ssh_config = _os.path.join(config, "ssh.config")
"""The path of the global ssh config file."""
ps_profile = _os.path.join(config, "powershell.ps1")
"""The path of the PowerShell profile file."""

# git
gitconfig = _os.path.join(config, ".gitconfig")
"""The path of the global gitconfig file."""
gitignore = _os.path.join(config, ".gitignore")
"""The path of the global gitignore file."""

# vscode
vscode = _os.path.join(config, "vscode")
"""The path of VSCode configuration directory."""
vscode_settings = _os.path.join(vscode, "settings.json")
"""The path of VSCode settings file."""
vscode_keybindings = _os.path.join(vscode, "keybindings.json")
"""The path of VSCode keybindings file."""
vscode_snippets = _os.path.join(vscode, "snippets")
"""The path of VSCode snippets directory."""
