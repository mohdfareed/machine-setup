"""Machine configuration files."""

import os as _os

import utils as _utils


def load_env_var(zshenv_path: str, var_name: str) -> str:
    """Load the environment variable value."""
    command = f"source {zshenv_path} && echo ${var_name}"
    return _utils.run(command)[1]


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

# private files
private_machine = load_env_var(zshenv, "PRIVATE_MACHINE")
"""The path of the machine private files directory."""
private_env = _os.path.join(private_machine, "env.sh")
"""The path of the machine private environment file."""
ssh_keys = _os.path.join(private_machine, "keys")
"""The path of the machine ssh keys directory."""

# xdg directories
xdg_config = load_env_var(zshenv, "XDG_CONFIG_HOME")
"""The path of the XDG configuration directory."""
zdotdir = load_env_var(zshenv, "ZDOTDIR")
"""The path of the ZDOTDIR directory."""

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
