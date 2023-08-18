"""Machine configuration files."""

import os as _os

# machine configuration directories
machine = _os.path.dirname(_os.path.realpath(__file__))
"""The path to the machine configuration directory."""
shell = _os.path.join(machine, "shell")
"""The path of shell configuration file."""
vim = _os.path.join(machine, "vim")
"""The path of vim configuration files."""
macos = _os.path.join(machine, "macos")
"""The path of macOS configuration directory."""
git = _os.path.join(machine, "git")
"""The path of git configuration directory."""
pi_machine = _os.path.join(_os.path.dirname(machine), "raspberrypi")
"""The path of Raspberry Pi configuration directory."""

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

# git
gitconfig = _os.path.join(git, "config")
"""The path of the global gitconfig file."""
gitignore = _os.path.join(git, "ignore")
"""The path of the global gitignore file."""

# packages
brewfile = _os.path.join(machine, "brewfile")
"""The path of Homebrew packages file."""
requirements = _os.path.join(machine, "requirements.txt")
"""The path of Python requirements file."""

# macos
macos_preferences = _os.path.join(macos, "preferences.sh")
"""The path of macOS preferences file of shell commands."""

# raspberry pi
pi_zprofile = _os.path.join(pi_machine, "zprofile")
"""The path of Raspberry Pi profile variables file."""
pi_zshenv = _os.path.join(pi_machine, "zshenv")
"""The path of Raspberry Pi environment variables file."""
pi_shared_config = (zsh_config, zsh_env, vim, tmux)
"""The shared config files between the machine and Raspberry Pi."""
