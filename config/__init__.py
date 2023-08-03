"""Machine configuration files."""

import os as _os

machine = _os.path.dirname(_os.path.realpath(__file__))
"""The path to the machine configuration directory."""

# shell
shell_env = _os.path.join(machine, "shell", "env.sh")
"""The path of the shell environment file."""
shell_config = _os.path.join(machine, "shell", "config.sh")
"""The path of the shell configuration file."""
zshrc = _os.path.join(machine, "shell", "zshrc")
"""The path of zshrc file."""
zshenv = _os.path.join(machine, "shell", "zshenv")
"""The path of zshenv file."""
micro_settings = _os.path.join(machine, "shell", "micro_settings.json")
"""The path of micro settings file."""

# git and ssh
gitconfig = _os.path.join(machine, "git", "gitconfig")
"""The path of the global gitconfig file."""
ssh_keys = _os.path.join(machine, "ssh")
"""The path of the SSH directory of keys."""

# packages
homebrew_packages = _os.path.join(machine, "packages.homebrew")
"""The path of Homebrew packages file."""
python_packages = _os.path.join(machine, "packages.python")
"""The path of Python packages file."""

# macos
macos_preferences = _os.path.join(machine, "macos", "preferences.sh")
"""The path of macOS preferences file of shell commands."""
terminal_dark = _os.path.join(machine, "macos", "terminal", "Dark.terminal")
terminal_light = _os.path.join(machine, "macos", "terminal", "Light.terminal")

# raspberry pi
pi_config = _os.path.join(_os.path.dirname(machine), "raspberrypi")
"""The path of Raspberry Pi config directory."""
pi_env = _os.path.join(pi_config, "env.sh")
"""The path of Raspberry Pi environment file."""
pi_zshenv = _os.path.join(pi_config, "zshenv")
"""The path of Raspberry Pi shell environment file."""
