"""Setup functions for various tools and utilities."""

__all__ = ["setup_docker", "setup_python", "setup_node", "setup_zed"]

import logging
import os
from typing import Optional, Union

import config
import utils
from scripts.package_managers import APT, HomeBrew, Scoop, WinGet

LOGGER = logging.getLogger(__name__)
"""The package managers logger."""


def setup(pkg_manager: Union[HomeBrew, APT, Scoop]) -> None:
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
        pkg_manager.install("docker", cask=True)
    elif isinstance(pkg_manager, WinGet):
        pkg_manager.install("Docker.DockerDesktop")
    elif utils.is_unix():
        utils.shell.run("curl -fsSL https://get.docker.com | sh")
    else:
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")
    LOGGER.debug("Docker was setup successfully.")


def setup_python(pkg_manager: Union[HomeBrew, APT, Scoop]) -> None:
    """Setup python on a new Debian machine."""
    LOGGER.info("Setting up Python...")

    if isinstance(pkg_manager, HomeBrew):
        pkg_manager.install("python pipx pyenv")
        utils.shell.run("pipx install poetry")

    if isinstance(pkg_manager, APT):
        pkg_manager.install("python3 python3-pip python3-venv pipx")
        if not utils.is_installed("pyenv"):
            utils.shell.run("curl https://pyenv.run | bash")
        utils.shell.run("pipx install poetry")

    if isinstance(pkg_manager, Scoop):
        # python is installed by default through winget
        pkg_manager.install("pipx pyenv")
        utils.shell.run("pipx install poetry")

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
        utils.shell.run(f"curl -o- {url} | bash")
    else:  # only on unix systems can there be no package manager
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")
    LOGGER.debug("Node was setup successfully.")


def setup_zed(pkg_manager: Optional[HomeBrew]) -> None:
    """Setup the Zed text editor on a new machine."""
    LOGGER.info("Setting up Zed...")
    if isinstance(pkg_manager, HomeBrew):
        pkg_manager.install("zed")
    elif utils.is_linux():
        utils.shell.run("curl -f https://zed.dev/install.sh | sh")
    else:
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")

    settings_file = os.path.join(config.xdg_config, "zed", "settings.json")
    utils.symlink(config.zed_settings, settings_file)
    LOGGER.debug("Zed was setup successfully.")


if __name__ == "__main__":
    raise RuntimeError("This script is not meant to be run directly.")
