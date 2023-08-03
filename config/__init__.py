"""Machine configuration files."""

import os as _os

# machine configuration files
machine = _os.path.dirname(_os.path.realpath(__file__))
"""The path to the machine configuration directory."""
zsh_config = _os.path.join(machine, "zsh_config.sh")
"""The path of the shared shell configuration file."""
zsh_env = _os.path.join(machine, "zsh_env.sh")
"""The path of the shared shell environment file."""
zshrc = _os.path.join(machine, "zshrc")
"""The path of zshrc file, macOS specific."""
zshenv = _os.path.join(machine, "zshenv")
"""The path of zshenv file, macOS specific."""
zprofile = _os.path.join(machine, "zprofile")
"""The path of the machine shell profile variables file."""
micro_settings = _os.path.join(machine, "micro_settings.json")
"""The path of micro settings file."""
ssh_config = _os.path.join(machine, "ssh.config")
"""The path of the global ssh config file."""
gitconfig = _os.path.join(machine, "gitconfig")
"""The path of the global gitconfig file."""
gitignore = _os.path.join(machine, "gitignore")
"""The path of the global gitignore file."""

# packages
homebrew_packages = _os.path.join(machine, "packages.homebrew")
"""The path of Homebrew packages file."""
python_packages = _os.path.join(machine, "packages.python")
"""The path of Python packages file."""

# macos
macos = _os.path.join(machine, "macos")
"""The path of macOS config directory."""
macos_preferences = _os.path.join(macos, "preferences.sh")
"""The path of macOS preferences file of shell commands."""
terminal_dark = _os.path.join(macos, "terminal", "Dark.terminal")
terminal_light = _os.path.join(macos, "terminal", "Light.terminal")

# raspberry pi
pi_config = _os.path.join(_os.path.dirname(machine), "raspberrypi")
"""The path of Raspberry Pi config directory."""
pi_zprofile = _os.path.join(pi_config, "zprofile")
"""The path of Raspberry Pi profile variables file."""
