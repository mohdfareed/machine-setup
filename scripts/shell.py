"""Setup module containing a `setup` function for setting up the shell on a new
machine.
"""

import glob
import logging
import os

import config
import utils

ZSHENV = "~/.zshenv"
"""The path to the zsh environment file symlink."""
ZSHRC = os.path.join(config.zdotdir, ".zshrc")
"""The path to the zsh configuration file symlink."""
VIM = os.path.join(config.xdg_config, "nvim")
"""The path of the vim configuration directory symlink."""
TMUX = os.path.join(config.xdg_config, "tmux", "tmux.conf")
"""The path of the tmux configuration file symlink."""

LOGGER = logging.getLogger(__name__)
"""The ZSH setup logger."""


def setup() -> None:
    """Setup the shell environment on a machine."""
    LOGGER.info("Setting up shell...")

    # install omz and symlink config files
    install_omz()
    utils.symlink(config.vim, VIM)
    utils.symlink(config.tmux, TMUX)
    utils.symlink(config.zshrc, ZSHRC)
    utils.symlink(config.zshenv, ZSHENV)

    # clean up
    utils.run("sudo rm -rf ~/.zcompdump*")
    utils.run("sudo rm -rf ~/.zshrc")
    utils.run("sudo rm -rf ~/.zsh_sessions")
    utils.run("sudo rm -rf ~/.zsh_history")
    LOGGER.info("Shell setup complete.")


def install_omz() -> None:
    """Install oh-my-zsh."""
    LOGGER.info("Installing oh-my-zsh...")

    # load installation environment
    cmd = f"source {config.zshenv} && echo $ZSH"
    env = dict(ZSH=utils.run(cmd)[1])

    # install oh-my-zsh
    utils.run(["sudo", "rm", "-rf", env["ZSH"]])  # remove existing files
    cmd = 'sh -c "$(curl -fsSL https://git.io/JvzfK)" "" --unattended'
    utils.run(cmd, env=env, msg="Installing")

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
    scripts.run_setup_isolated(setup)
