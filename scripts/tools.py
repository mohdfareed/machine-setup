"""Setup functions for various tools and utilities."""

__all__ = [
    "setup_docker",
    "setup_python",
    "setup_node",
    "setup_zed",
    "install_btop",
    "install_powershell",
    "install_nvim",
]

import logging
import os
from typing import Optional, Union

import config
import utils
from scripts.package_managers import APT, HomeBrew, Scoop, SnapStore, WinGet

LOGGER = logging.getLogger(__name__)
"""The package managers logger."""


def setup_fonts(pkg_manager: Union[HomeBrew, APT, Scoop]) -> None:
    """Setup fonts on a new machine."""
    LOGGER.info("Setting up tailscale...")
    if isinstance(pkg_manager, HomeBrew):
        pkg_manager.install("font-computer-modern font-jetbrains-mono-nerd-font")
    elif isinstance(pkg_manager, APT):
        pkg_manager.install("fonts-jetbrains-mono fonts-lmodern")
    else:
        pkg_manager.add_bucket("nerd-fonts")
        pkg_manager.install("nerd-fonts/JetBrains-Mono")
    LOGGER.debug("Fonts were setup successfully.")


def setup_docker(pkg_manager: Optional[Union[HomeBrew, WinGet]]) -> None:
    """Setup docker on a new Debian machine."""
    LOGGER.info("Setting up Docker...")
    if isinstance(pkg_manager, HomeBrew):
        # REVIEW: check homebrew cask for apple silicon support
        LOGGER.warning("Docker is not supported on Apple Silicon.")
        LOGGER.warning("Download manually from: https://www.docker.com")
    elif isinstance(pkg_manager, WinGet):
        pkg_manager.install("Docker.DockerDesktop")
    elif utils.is_unix():
        utils.shell.execute("curl -fsSL https://get.docker.com | sh")
    else:
        raise utils.Unsupported(f"Unsupported operating system: {utils.OS}")
    LOGGER.debug("Docker was setup successfully.")


def setup_python(pkg_manager: Union[HomeBrew, APT, Scoop]) -> None:
    """Setup python on a new Debian machine."""
    LOGGER.info("Setting up Python...")

    if isinstance(pkg_manager, HomeBrew):
        pkg_manager.install("python pipx pyenv")
        utils.shell.execute("pipx install poetry")

    if isinstance(pkg_manager, APT):
        pkg_manager.install("python3 python3-pip python3-venv pipx")
        if not utils.is_installed("pyenv"):
            utils.shell.execute("curl https://pyenv.run | bash")
        utils.shell.execute("pipx install poetry")

    if isinstance(pkg_manager, Scoop):
        # python is installed by default through winget
        pkg_manager.install("pipx pyenv")
        utils.shell.execute("pipx install poetry")

    # install poetry completions
    if config.shell_completions and utils.is_installed("poetry"):
        utils.shell.execute(
            f"poetry completions zsh > {config.shell_completions}/_poetry"
        )
    LOGGER.debug("Python was setup successfully.")


def setup_node(pkg_manager: Optional[Union[HomeBrew, WinGet]]) -> None:
    """Setup node on a new Debian machine."""
    LOGGER.info("Setting up Node...")

    if isinstance(pkg_manager, HomeBrew):
        pkg_manager.install("nvm")
    elif isinstance(pkg_manager, WinGet):
        pkg_manager.install("Schniz.fnm")
    elif utils.is_unix() and not utils.is_installed("nvm"):
        url = "https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh"
        utils.shell.execute(f"curl -o- {url} | bash")
    else:  # only on unix systems can there be no package manager
        raise utils.Unsupported(f"Unsupported operating system: {utils.OS}")
    LOGGER.debug("Node was setup successfully.")


def setup_zed(pkg_manager: Optional[HomeBrew]) -> None:
    """Setup the Zed text editor on a new machine."""
    LOGGER.info("Setting up Zed...")
    if not config.xdg_config:
        raise utils.Unsupported(f"Unsupported operating system: {utils.OS}")

    if isinstance(pkg_manager, HomeBrew):
        pkg_manager.install("zed")
    elif utils.is_linux():
        utils.shell.execute("curl -f https://zed.dev/install.sh | sh")

    settings_file = os.path.join(config.xdg_config, "zed", "settings.json")
    utils.symlink(config.zed_settings, settings_file)
    LOGGER.debug("Zed was setup successfully.")


def install_btop(pkg_manager: Union[HomeBrew, Scoop, SnapStore]) -> None:
    """Install btop on a machine."""
    if isinstance(pkg_manager, HomeBrew):
        pkg_manager.install("btop")
    if isinstance(pkg_manager, Scoop):
        pkg_manager.install("btop-lhm")
    if isinstance(pkg_manager, SnapStore):
        pkg_manager.install("btop")


def install_powershell(pkg_manager: Union[HomeBrew, WinGet, SnapStore]) -> None:
    """Install PowerShell on a machine."""
    if isinstance(pkg_manager, HomeBrew):
        pkg_manager.install("powershell", cask=True)
    if isinstance(pkg_manager, WinGet):
        pkg_manager.install("Microsoft.PowerShell")
    if isinstance(pkg_manager, SnapStore):
        pkg_manager.install("powershell")


def install_nvim(pkg_manager: Union[HomeBrew, WinGet, SnapStore]) -> None:
    """Install NeoVim on a machine."""
    if isinstance(pkg_manager, HomeBrew):
        pkg_manager.install("nvim")
    if isinstance(pkg_manager, WinGet):
        pkg_manager.install("Neovim.Neovim")
    if isinstance(pkg_manager, SnapStore):
        pkg_manager.install("nvim")
