"""Setup module containing a `setup` function for setting up the shell on a new
machine.
"""

import logging
import os

import config
import utils
from utils import shell

ZSHENV = "~/.zshenv"
"""The path to the zsh environment file symlink."""

LOGGER = logging.getLogger(__name__)
"""The ZSH setup logger."""


def setup(zshrc=config.zshrc, zshenv=config.zshenv) -> None:
    """Setup the shell environment on a machine."""
    LOGGER.info("Setting up shell...")

    if not os.path.exists(zshrc):
        LOGGER.error("Machine zshrc file does not exist.")
        return
    if not os.path.exists(zshenv):
        LOGGER.error("Machine zshenv file does not exist.")
        return

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

    # TODO: update zinit plugins

    # clean up
    shell.run("sudo rm -rf ~/.zcompdump*")
    shell.run("sudo rm -rf ~/.zshrc")
    shell.run("sudo rm -rf ~/.zsh_sessions")
    shell.run("sudo rm -rf ~/.zsh_history")
    LOGGER.info("Shell setup complete.")


if __name__ == "__main__":
    utils.PARSER.add_argument(
        "zshrc",
        help="The path to the zshrc file.",
        nargs="?",
        default=config.zshrc,
    )
    utils.PARSER.add_argument(
        "zshenv",
        help="The path to the zshenv file.",
        nargs="?",
        default=config.zshenv,
    )

    args = utils.startup(description="Shell setup script.")
    utils.execute(setup, args.machine_zshrc, args.machine_zshenv)
