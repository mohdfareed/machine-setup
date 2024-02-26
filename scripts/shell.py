"""Setup module containing a `setup` function for setting up the shell on a new
machine.
"""

import glob
import logging
import os

import config
import utils

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


def setup() -> None:
    """Setup the shell environment on a machine."""
    LOGGER.info("Setting up shell...")

    # install omz and symlink config files
    install_omz()
    utils.symlink(config.zshrc, ZSHRC)
    utils.symlink(config.zshenv, ZSHENV)
    utils.symlink(config.tmux, TMUX)
    utils.symlink(config.vim, VIM, is_dir=True)

    # disable login message
    utils.run_cmd("touch ~/.hushlogin")
    LOGGER.info("Shell setup complete")


def install_omz():
    LOGGER.info("Installing oh-my-zsh...")

    # load installation environment
    cmd = f"source {config.zsh_env} && echo $ZSH"
    env = dict(ZSH=utils.run_cmd(cmd)[1])

    # install oh-my-zsh
    utils.run_cmd(["sudo", "rm", "-rf", env["ZSH"]])  # remove existing files
    cmd = 'sh -c "$(curl -fsSL https://git.io/JvzfK)" "" --unattended'
    utils.run_cmd(cmd, env=env, msg="Installing")

    # remove zshrc backup files
    backups = os.path.expanduser(f"{ZSHRC}.pre-oh-my-zsh*")
    for filename in glob.glob(backups, include_hidden=True):
        os.remove(filename)

    LOGGER.debug("Installed oh-my-zsh.")


if __name__ == "__main__":
    import argparse

    import scripts

    parser = argparse.ArgumentParser(description="Shell setup script.")
    args = parser.parse_args()
    scripts.run_setup(setup)
