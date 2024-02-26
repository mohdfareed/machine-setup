"""Machine configuration files."""

import os as _os

# machine configuration directories
config = _os.path.dirname(_os.path.realpath(__file__))
"""The path to the machine configuration directory."""
shell = _os.path.join(config, "shell")
"""The path of shell configuration file."""
vim = _os.path.join(config, "vim")
"""The path of vim configuration files."""
macos = _os.path.join(config, "macos")
"""The path of macOS configuration directory."""
git = _os.path.join(config, "git")
"""The path of git configuration directory."""
vscode = _os.path.join(config, "vscode")
"""The path of VSCode configuration directory."""
pi_machine = _os.path.join(_os.path.dirname(config), "raspberrypi")
"""The path of Raspberry Pi configuration directory."""
private_machine = "$PRIVATE_MACHINE"
"""The path of the private machine configuration directory."""

# shell
zsh_config = _os.path.join(shell, "config.sh")
"""The path of the shared shell configuration file."""
zsh_env = _os.path.join(shell, "env.sh")
"""The path of the shared shell environment file."""
zshrc = _os.path.join(shell, "zshrc")
"""The path of zshrc file, macOS specific."""
zshenv = _os.path.join(shell, "zshenv")
"""The path of zshenv file, macOS specific."""
zprofile = _os.path.join(shell, "zprofile")
"""The path of the machine shell profile variables file."""
ssh_config = _os.path.join(shell, "ssh.config")
"""The path of the global ssh config file."""
tmux = _os.path.join(shell, "tmux.conf")
"""The path of the tmux configuration file."""
private_env = _os.path.join(private_machine, "env.sh")
"""The path of the private machine environment file."""

# git
gitconfig = _os.path.join(git, "config")
"""The path of the global gitconfig file."""
gitignore = _os.path.join(git, "ignore")
"""The path of the global gitignore file."""

# packages
brewfile = _os.path.join(config, "brewfile")
"""The path of Homebrew packages file."""
requirements = _os.path.join(config, "requirements.txt")
"""The path of Python requirements file."""

# macos
macos_preferences = _os.path.join(macos, "preferences.sh")
"""The path of macOS preferences file of shell commands."""

# vscode
vscode_settings = _os.path.join(vscode, "settings.json")
"""The path of VSCode settings file."""
vscode_keybindings = _os.path.join(vscode, "keybindings.json")
"""The path of VSCode keybindings file."""

# raspberry pi
pi_zprofile = _os.path.join(pi_machine, "zprofile")
"""The path of Raspberry Pi profile variables file."""
pi_zshenv = _os.path.join(pi_machine, "zshenv")
"""The path of Raspberry Pi environment variables file."""
pi_shared_config = (zsh_config, zsh_env, vim, tmux)
"""The shared config files between the machine and Raspberry Pi."""
