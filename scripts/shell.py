"""Setup module containing a `setup` function for setting up the shell on a new
machine.
"""

import glob
import logging
import os

import config
import utils
from utils import shell

ZSHENV = "~/.zshenv"
"""The path to the zsh environment file symlink."""

LOGGER = logging.getLogger(__name__)
"""The ZSH setup logger."""


def setup(
    xdg_config: str | None = None,
    zdotdir: str | None = None,
    machine_zshrc=config.zshrc,
    machine_zshenv=config.zshenv,
) -> None:
    """Setup the shell environment on a machine."""
    LOGGER.info("Setting up shell...")

    if xdg_config is None:
        xdg_config = shell.run("echo $XDG_CONFIG_HOME")[1]
    if not xdg_config:
        xdg_config = os.path.expanduser("~/.config")

    if zdotdir is None:
        zdotdir = shell.run("echo $ZDOTDIR")[1]
    if not zdotdir:
        zdotdir = os.path.expanduser("~/.config/zsh")

    # resolve shell configuration paths
    zshrc = os.path.join(zdotdir, ".zshrc")
    vim = os.path.join(xdg_config, "nvim")
    tmux = os.path.join(xdg_config, "tmux", "tmux.conf")
    ps_profile = os.path.join(xdg_config, "powershell", "profile.ps1")

    # install omz and symlink config files
    install_omz(zshrc)
    utils.symlink(config.vim, vim)
    utils.symlink(config.tmux, tmux)
    utils.symlink(config.ps_profile, ps_profile)
    utils.symlink(machine_zshrc, zshrc)
    utils.symlink(machine_zshenv, ZSHENV)

    # dotnet and uno setup
    dotnet_path = utils.load_env_var(ZSHENV, "DOTNET_ROOT")
    shell.run(f"{dotnet_path}/dotnet tool install -g uno.check")
    shell.run(f"{dotnet_path}/dotnet tool update -g uno.check")

    # clean up
    shell.run("sudo rm -rf ~/.zcompdump*")
    shell.run("sudo rm -rf ~/.zshrc")
    shell.run("sudo rm -rf ~/.zsh_sessions")
    shell.run("sudo rm -rf ~/.zsh_history")
    LOGGER.info("Shell setup complete.")


def install_omz(current_zshrc) -> None:
    """Install oh-my-zsh. Overwrites current zshrc file."""
    LOGGER.info("Installing oh-my-zsh...")

    # load installation environment
    cmd = f"source {config.zshenv} && echo $ZSH"
    env = dict(ZSH=shell.run(cmd)[1])

    # install oh-my-zsh
    shell.run(["sudo", "rm", "-rf", env["ZSH"]])  # remove existing files
    cmd = 'sh -c "$(curl -fsSL https://git.io/JvzfK)" "" --unattended'
    shell.run(cmd, env=env, msg="Installing")

    # remove zshrc backup files
    backups = os.path.expanduser(f"{current_zshrc}.pre-oh-my-zsh*")
    for filename in glob.glob(backups, include_hidden=True):
        os.remove(filename)

    LOGGER.debug("Installed oh-my-zsh.")


if __name__ == "__main__":
    utils.PARSER.add_argument(
        "xdg_config",
        help="The path to the XDG configuration directory.",
        nargs="?",
        default=None,
    )
    utils.PARSER.add_argument(
        "zdotdir",
        help="The path to the ZDOTDIR directory.",
        nargs="?",
        default=None,
    )
    utils.PARSER.add_argument(
        "--machine-zshrc",
        help="The path to the machine specific zshrc file.",
        default=config.zshrc,
    )
    utils.PARSER.add_argument(
        "--machine-zshenv",
        help="The path to the machine specific zshenv file.",
        default=config.zshenv,
    )

    args = utils.startup(description="Shell setup script.")
    utils.execute(
        setup,
        args.xdg_config,
        args.zdotdir,
        args.machine_zshrc,
        args.machine_zshenv,
    )
