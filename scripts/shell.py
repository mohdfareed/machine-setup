"""Setup module containing a `setup` function for setting up the shell on a new
machine.
"""

import logging
import os

import config
import utils
from utils import shell
from utils.helpers import SetupError

if utils.is_windows():
    PS_PROFILE = os.path.join(
        os.environ["USERPROFILE"],
        "Documents",
        "WindowsPowerShell",
        "profile.ps1",
    )
    """The path to the PowerShell profile file."""
else:
    ZSHENV = os.path.join(os.path.expanduser("~"), ".zshenv")
    """The path to the zsh environment file symlink."""

LOGGER = logging.getLogger(__name__)
"""The ZSH setup logger."""


def setup(zshrc=config.zshrc, zshenv=config.zshenv) -> None:
    """Setup the shell environment on a machine."""

    if not utils.is_unix():
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")
    if not os.path.exists(zshrc):
        raise SetupError("Machine zshrc file does not exist.")
    if not os.path.exists(zshenv):
        raise SetupError("Machine zshenv file does not exist.")
    LOGGER.info("Setting up shell...")

    # resolve shell configuration paths
    _zshrc = os.path.join(config.zdotdir, ".zshrc")
    vim = os.path.join(config.xdg_config, "nvim")
    tmux = os.path.join(config.xdg_config, "tmux", "tmux.conf")
    ps_profile = os.path.join(config.xdg_config, "powershell", "profile.ps1")

    # symlink config files
    utils.symlink(config.vim, vim)
    utils.symlink(config.tmux, tmux)
    utils.symlink(config.ps_profile, ps_profile)
    utils.symlink(zshrc, _zshrc)
    utils.symlink(zshenv, ZSHENV)

    # TODO: update zinit and its plugins

    # clean up
    shell.run("sudo rm -rf ~/.zcompdump*", throws=False)
    shell.run("sudo rm -rf ~/.zshrc", throws=False)
    shell.run("sudo rm -rf ~/.zsh_sessions", throws=False)
    shell.run("sudo rm -rf ~/.zsh_history", throws=False)
    shell.run("sudo rm -rf ~/.lesshst", throws=False)
    LOGGER.info("Shell setup complete.")


def setup_windows(ps_profile=config.ps_profile) -> None:
    """Setup the shell environment on a Windows machine."""
    LOGGER.info("Setting up shell...")

    if not utils.is_windows():
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")
    if not os.path.exists(ps_profile):
        raise SetupError("Machine powershell profile file does not exist.")
    LOGGER.info("Setting up shell...")

    # resolve shell configuration paths
    vim = os.path.join(config.local_data, "nvim")

    # symlink config files
    utils.symlink(config.vim, vim)
    utils.symlink(config.ps_profile, PS_PROFILE)


if __name__ == "__main__":
    if utils.is_windows():
        utils.PARSER.add_argument(
            "ps_profile",
            help="The path to the PowerShell profile file.",
            nargs="?",  # optional argument
            default=config.ps_profile,
        )
    else:
        utils.PARSER.add_argument(
            "zshrc",
            help="The path to the zshrc file.",
            nargs="?",  # optional argument
            default=config.zshrc,
        )
        utils.PARSER.add_argument(
            "zshenv",
            help="The path to the zshenv file.",
            nargs="?",  # optional argument
            default=config.zshenv,
        )

    args = utils.startup(description="Shell setup script.")
    if utils.is_windows():
        utils.execute(setup_windows, args.ps_profile)
    else:
        utils.execute(setup, args.machine_zshrc, args.machine_zshenv)
