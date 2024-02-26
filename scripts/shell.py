"""Setup module containing a `setup` function for setting up the shell on a new
machine.
"""

import logging

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
    utils.symlink(config.zprofile, ZPROFILE)
    utils.symlink(config.tmux, TMUX)
    utils.symlink(config.vim, VIM, is_dir=True)

    # disable login message
    utils.run_shell("touch ~/.hushlogin")
    LOGGER.info("Shell setup complete")


def install_omz():
    LOGGER.info("Installing oh-my-zsh...")

    # load installation environment
    cmd = f"source {config.zsh_env} && echo $ZSH"
    env = dict(ZSH=utils.run_shell(cmd)[0])

    # install oh-my-zsh
    utils.run_shell(["sudo", "rm", "-rf", env["ZSH"]])  # remove existing files
    cmd = 'sh -c "$(curl -fsSL https://git.io/JvzfK)" "" --unattended'
    utils.run_shell(cmd, env=env, msg="Installing")

    # setup private shell environment
    cmd = f"echo {config.private_env}"
    private_ = dict(ZSH=utils.run_shell(cmd)[0])
    utils.symlink(config.zsh_env, f"{env['ZSH']}/.zshenv")

    # remove zshrc backup file
    utils.run_shell(["rm", "-rf", f"{ZSHRC}.pre-oh-my-zsh"])
    LOGGER.debug("Installed oh-my-zsh.")


if __name__ == "__main__":
    import argparse

    import scripts

    parser = argparse.ArgumentParser(description="Shell setup script.")
    args = parser.parse_args()
    scripts.run_setup(setup)
