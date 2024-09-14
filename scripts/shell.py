"""Setup module containing a `setup` function for setting up the shell on a new
machine.
"""

import logging
import os

import config
import scripts
import scripts.package_managers
import utils
from utils import shell
from utils.helpers import SetupError

LOGGER = logging.getLogger(__name__)
"""The ZSH setup logger."""

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
    ZDOTDIR = utils.load_env_var(config.zshenv, "ZDOTDIR")
    """The path of the ZDOTDIR directory on the machine."""


def setup(zshrc=config.zshrc, zshenv=config.zshenv) -> None:
    """Setup the shell environment on a machine."""

    if not utils.is_unix():
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")
    if not os.path.exists(zshrc):
        raise SetupError("Machine zshrc file does not exist.")
    if not os.path.exists(zshenv):
        raise SetupError("Machine zshenv file does not exist.")

    LOGGER.info("Setting up shell...")
    _install_unix_dependencies()

    # resolve shell configuration paths
    _zshrc = os.path.join(ZDOTDIR, ".zshrc")
    vim = os.path.join(config.xdg_config, "nvim")
    tmux = os.path.join(config.xdg_config, "tmux", "tmux.conf")
    ps_profile = os.path.join(config.xdg_config, "powershell", "profile.ps1")

    # symlink config files
    utils.symlink(config.vim, vim)
    utils.symlink(config.tmux, tmux)
    utils.symlink(config.ps_profile, ps_profile)
    utils.symlink(zshrc, _zshrc)
    utils.symlink(zshenv, ZSHENV)

    # update zinit and its plugins
    source_env = f"source {zshrc} && source {zshenv}"
    shell.run(f"{source_env} && zinit self-update && zinit update")

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
    _install_windows_dependencies()

    # resolve shell configuration paths
    vim = os.path.join(config.local_data, "nvim")

    # symlink config files
    utils.symlink(config.vim, vim)
    utils.symlink(config.ps_profile, PS_PROFILE)


def _install_windows_dependencies() -> None:
    install_powershell()
    if scripts.winget.try_install("Neovim.Neovim"):
        return
    if scripts.scoop.try_install("neovim"):
        return


def _install_unix_dependencies() -> None:
    install_powershell()
    if scripts.brew.try_install("zsh nvim btop"):
        return
    if scripts.apt.try_install("zsh"):
        if not scripts.snap.try_install("nvim btop"):
            LOGGER.error("Could not install nvim or btop.")
        return
    LOGGER.error("Could not install shell dependencies.")


def install_powershell() -> None:
    """Install PowerShell on a machine."""
    if scripts.brew.try_install("powershell", cask=True):
        return
    if scripts.winget.try_install("Microsoft.PowerShell"):
        return
    if scripts.snap.try_install("powershell"):
        return


def install_nvim() -> None:
    """Install NeoVim on a machine."""
    if scripts.winget.try_install("Neovim.Neovim"):
        return
    if scripts.brew.try_install("nvim"):
        return
    if scripts.snap.try_install("nvim btop"):
        return


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
