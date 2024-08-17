"""Machine configuration files."""

import os as _os

import utils as _utils

# machine configuration directories
config = _os.path.dirname(_os.path.realpath(__file__))
"""The path to the machine configuration directory."""
git = _os.path.join(config, "git")
"""The path of git configuration directory."""
vim = _os.path.join(config, "vim")
"""The path of vim configuration files."""
vscode = _os.path.join(config, "vscode")
"""The path of VSCode configuration directory."""

# shell, ssh, tmux, powershell
zshrc = _os.path.join(config, "zshrc")
"""The path of zshrc file."""
zshenv = _os.path.join(config, "zshenv")
"""The path of zshenv file."""
ssh_config = _os.path.join(config, "ssh.config")
"""The path of the global ssh config file."""
tmux = _os.path.join(config, "tmux.conf")
"""The path of the tmux configuration file."""
npmrc = _os.path.join(config, "npmrc")
"""The path of the npm configuration file."""
ps_profile = _os.path.join(config, "profile.ps1")
"""The path of the PowerShell profile file."""

# git
gitconfig = _os.path.join(git, "gitconfig")
"""The path of the global gitconfig file."""
gitignore = _os.path.join(git, "gitignore")
"""The path of the global gitignore file."""

# macos
brewfile = _os.path.join(config, "brewfile")
"""The path of Homebrew packages file."""
requirements = _os.path.join(config, "requirements.txt")
"""The path of Python requirements file."""
macos_preferences = _os.path.join(config, "preferences.sh")
"""The path of macOS preferences file of shell commands."""

# vscode
vscode_settings = _os.path.join(vscode, "settings.json")
"""The path of VSCode settings file."""
vscode_keybindings = _os.path.join(vscode, "keybindings.json")
"""The path of VSCode keybindings file."""
vscode_snippets = _os.path.join(vscode, "snippets")
"""The path of VSCode snippets directory."""

# private files
cmd = f"source {zshenv} && echo $PRIVATE_MACHINE"
private_machine = _utils.run_cmd(cmd)[1]
"""The path of the machine private files directory."""
private_env = _os.path.join(private_machine, "env.sh")
"""The path of the machine private environment file."""
private_pi_env = _os.path.join(private_machine, "pi.sh")
"""The path of the Raspberry Pi private environment file."""
ssh_keys = _os.path.join(private_machine, "keys")
"""The path of the machine ssh keys directory."""

# xdg directories
cmd = f"source {zshenv} && echo $XDG_CONFIG_HOME"
xdg_config = _utils.run_cmd(cmd)[1]
"""The path of the XDG configuration directory."""
cmd = f"source {zshenv} && echo $ZDOTDIR"
zdotdir = _utils.run_cmd(cmd)[1]
"""The path of the ZDOTDIR directory."""
cmd = f"source {zshenv} && echo $NPM_CONFIG_USERCONFIG"
npm_config_userconfig = _utils.run_cmd(cmd)[1]
"""The path of the npm configuration file."""
