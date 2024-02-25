"""Setup module containing a `setup` function for setting up the shell on a new
machine.
"""

import logging
import os

import config
from utils.shell import Shell

ZPROFILE = "~/.zprofile"
"""The path to the zsh profile file symlink."""
ZSHRC = "~/.zshrc"
"""The path to the zsh configuration file symlink."""
ZSHENV = "~/.zshenv"
"""The path to the zsh environment file symlink."""
VIM = "~/.config/nvim"
"""The path of the vim configuration directory symlink."""
TMUX = "~/.tmux.conf"
"""The path of the tmux configuration file symlink."""

LOGGER = logging.getLogger(__name__)
"""The ZSH setup logger."""
shell = Shell(LOGGER.debug, LOGGER.error)
"""The ZSH shell instance."""


def setup() -> None:
    """Setup the shell environment on a machine."""
    LOGGER.info("Setting up shell...")

    # install omz and symlink config files
    install_omz()
    os.makedirs(os.path.dirname(ZSHRC), exist_ok=True)
    os.makedirs(os.path.dirname(VIM), exist_ok=True)
    os.remove(ZSHRC)
    os.symlink(config.zshrc, ZSHRC)
    os.remove(ZSHENV)
    os.symlink(config.zshenv, ZSHENV)
    os.remove(ZPROFILE)
    os.symlink(config.zprofile, ZPROFILE)
    os.remove(TMUX)
    os.symlink(config.tmux, TMUX)
    os.remove(VIM)
    os.symlink(config.vim, VIM)

    # disable login message
    shell("touch ~/.hushlogin", silent=True)
    LOGGER.info("Shell setup complete")


def install_omz():
    LOGGER.info("Installing oh-my-zsh...")

    # load installation environment
    cmd = f"source {config.zsh_env} && echo $ZSH"
    env = dict(ZSH=shell(cmd, silent=True)[0])

    # install oh-my-zsh
    shell(["sudo", "rm", "-rf", env["ZSH"]])
    cmd = 'sh -c "$(curl -fsSL https://git.io/JvzfK)" "" --unattended'
    if shell(cmd, env=env, silent=True, status="Installing...")[1] != 0:
        raise RuntimeError("Failed to install oh-my-zsh")

    # terminal theme
    # TODO: backup iTerm2 theme/settings
    # curl -s -N 'https://warp-themes.com/d/sE6RPpSXOCX6nJunRoUt' | bash

    # remove zshrc backup file
    shell(["rm", "-rf", f"{ZSHRC}.pre-oh-my-zsh"])
    LOGGER.debug("Installed oh-my-zsh")


if __name__ == "__main__":
    import argparse

    import core

    parser = argparse.ArgumentParser(description="Shell setup script.")
    args = parser.parse_args()
    core.run(setup, LOGGER, "Failed to setup shell")
