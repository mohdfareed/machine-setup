"""Machine configuration files."""

import logging as _logging
import os as _os

import utils as _utils

LOGGER = _logging.getLogger(__name__)
"""The machine configuration logger."""

config = _os.path.dirname(_os.path.realpath(__file__))
"""The path to the machine configuration directory."""

# configuration files =========================================================

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

ps_profile = _os.path.join(config, "ps_profile.ps1")
"""The path of the PowerShell profile file."""

tmux = _os.path.join(config, "tmux.conf")
"""The path of the tmux configuration file."""

zshrc = _os.path.join(config, "zshrc")
"""The path of zshrc file."""
zshenv = _os.path.join(config, "zshenv")
"""The path of zshenv file."""

# environment variables =======================================================

MACHINE = _utils.load_env_var(
    ps_profile if _utils.is_windows() else zshenv, "MACHINE"
)
"""The path to the machine repository."""

private_env = _utils.load_env_var(
    ps_profile if _utils.is_windows() else zshenv, "PRIVATE_ENV"
)
"""The path of the machine private environment file."""

ssh_keys = _utils.load_env_var(
    ps_profile if _utils.is_windows() else zshenv, "SSH_KEYS"
)
"""The path of the machine ssh keys directory."""

# os-specific environment variables ===========================================

if _utils.is_windows():
    local_data = _utils.load_env_var(ps_profile, "LOCALAPPDATA")
    """The path of the Windows local data directory."""

else:  # unix systems
    xdg_config = _utils.load_env_var(zshenv, "XDG_CONFIG_HOME")
    """The path of the XDG configuration directory."""

    zdotdir = _utils.load_env_var(zshenv, "ZDOTDIR")
    """The path of the ZDOTDIR directory."""


# helper functions ============================================================


def link_private_config(private_machine: str) -> None:
    """Load private machine configuration."""
    LOGGER.info("Loading private machine configuration: %s", private_machine)
    source_env = _os.path.join(private_machine, _os.path.basename(private_env))
    source_keys = _os.path.join(private_machine, _os.path.basename(ssh_keys))

    try:  # symlink private environment
        _utils.symlink(source_env, private_env)
    except FileNotFoundError:
        LOGGER.warning("Private environment not found.")
    try:  # symlink SSH keys
        _utils.symlink(source_keys, ssh_keys)
    except FileNotFoundError:
        LOGGER.warning("SSH keys not found.")


def report(machine_config: dict[str, str] | None) -> None:
    """Report the machine configuration.
    Args:
        machine_config (dict[str, str]): Additional configuration.
    """

    LOGGER.debug("Machine configuration:")
    LOGGER.debug("MACHINE: %s", MACHINE)
    LOGGER.debug("PRIVATE_ENV: %s", private_env)
    LOGGER.debug("SSH_KEYS: %s", ssh_keys)

    if _utils.is_unix():
        LOGGER.debug("XDG_CONFIG_HOME: %s", xdg_config)
        LOGGER.debug("ZDOTDIR: %s", zdotdir)

    if machine_config:
        LOGGER.debug("Additional configuration:")
        for key, value in machine_config.items():
            LOGGER.debug("%s: %s", key, value)
    LOGGER.debug("Machine configuration reported.")
