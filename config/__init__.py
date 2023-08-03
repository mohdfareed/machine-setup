"""Machine configuration files."""

import os as _os

machine = _os.path.dirname(_os.path.realpath(__file__))
"""The path to the machine configuration directory."""
shell = _os.path.join(machine, "shell")
"""The path to the shell configuration directory."""
macos = _os.path.join(machine, "macos")
"""The path to the macOS configuration directory."""

# shell configuration files
shell_env = _os.path.join(shell, "env.sh")
"""The path of the shell environment file."""
shell_config = _os.path.join(shell, "config.sh")
"""The path of the shell configuration file."""
zshrc = _os.path.join(shell, "zshrc")
"""The path of zshrc file."""
zshenv = _os.path.join(shell, "zshenv")
"""The path of zshenv file."""
micro_settings = _os.path.join(shell, "micro_settings.json")
"""The path of micro settings file."""
ssh_config = _os.path.join(shell, "ssh.config")
"""The path of the global ssh config file."""
gitconfig = _os.path.join(machine, "git", "gitconfig")
"""The path of the global gitconfig file."""

# packages
homebrew_packages = _os.path.join(machine, "packages.homebrew")
"""The path of Homebrew packages file."""
python_packages = _os.path.join(machine, "packages.python")
"""The path of Python packages file."""

# macos
macos_preferences = _os.path.join(macos, "preferences.sh")
"""The path of macOS preferences file of shell commands."""
terminal_dark = _os.path.join(macos, "terminal", "Dark.terminal")
terminal_light = _os.path.join(macos, "terminal", "Light.terminal")

# raspberry pi
pi_config = _os.path.join(_os.path.dirname(machine), "raspberrypi")
"""The path of Raspberry Pi config directory."""
pi_env = _os.path.join(pi_config, "env.sh")
"""The path of Raspberry Pi environment file."""
pi_zshenv = _os.path.join(pi_config, "zshenv")
"""The path of Raspberry Pi shell environment file."""
