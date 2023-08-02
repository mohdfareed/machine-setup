"""Machine configuration files."""

import os

_config = os.path.dirname(os.path.realpath(__file__))
"""The path to the resources directory."""

# shell
shell_config = os.path.join(_config, "shell", "config.sh")
"""The path of the shell config file."""
zshrc = os.path.join(_config, "shell", "zshrc")
"""The path of zshrc file."""
micro_settings = os.path.join(_config, "shell", "micro_settings.json")
"""The path of micro settings file."""
zshenv = os.path.join(_config, "shell", "zshenv")
"""The path of shell environment file."""
ssh_keys = os.path.join(_config, "ssh")
"""The path of the SSH directory of keys."""
gitconfig = os.path.join(_config, "git", "gitconfig")
"""The path of the global gitconfig file."""

# packages
homebrew_packages = os.path.join(_config, "packages.homebrew")
"""The path of Homebrew packages file."""
python_packages = os.path.join(_config, "packages.python")
"""The path of Python packages file."""

# macos
macos_preferences = os.path.join(_config, "macos", "preferences.sh")
"""The path of macOS preferences file of shell commands."""
terminal_dark = os.path.join(_config, "macos", "terminal", "Dark.terminal")
terminal_light = os.path.join(_config, "macos", "terminal", "Light.terminal")

# raspberry pi
raspberrypi_config = os.path.join(os.path.dirname(_config), "raspberrypi")
"""The path of Raspberry Pi config directory."""
raspberrypi_zshenv = os.path.join(raspberrypi_config, "zshenv")
"""The path of Raspberry Pi shell environment file."""
