"""Library of modules containing setup methods used for setting up a new
machine. These methods are imported and used by the main `setup.py` script. The
modules in this library depend on modules in the `utils` library."""

import logging

import utils
from scripts.package_managers import *

LOGGER = logging.getLogger(__name__)
"""The package managers logger."""


def setup_docker(pkg_manager: HomeBrew | WinGet | None) -> None:
    """Setup docker on a new Debian machine."""
    LOGGER.info("Setting up Docker...")

    if isinstance(pkg_manager, HomeBrew):
        pkg_manager.install("docker", cask=True)
        LOGGER.debug("Docker was setup successfully.")
        return

    if isinstance(pkg_manager, WinGet):
        pkg_manager.install("Docker.DockerDesktop")
        LOGGER.debug("Docker was setup successfully.")
        return

    if utils.is_unix():
        utils.shell.run("curl -fsSL https://get.docker.com | sh")
        return

    raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")


def setup_python(pkg_manager: HomeBrew | APT | Scoop) -> None:
    """Setup python on a new Debian machine."""
    LOGGER.info("Setting up Python...")

    if isinstance(pkg_manager, HomeBrew):
        pkg_manager.install("python pipx pyenv")

    if isinstance(pkg_manager, APT):
        pkg_manager.install("python3 python3-pip python3-venv pipx")
        if not utils.is_installed("pyenv"):
            utils.shell.run("curl https://pyenv.run | bash")

    if isinstance(pkg_manager, Scoop):
        # python is installed by default when running the script
        # it is done through winget
        pkg_manager.install("pipx pyenv")

    LOGGER.debug("Python was setup successfully.")


def setup_node(pkg_manager: HomeBrew | WinGet | None) -> None:
    """Setup node on a new Debian machine."""
    LOGGER.info("Setting up Node...")

    if isinstance(pkg_manager, HomeBrew):
        pkg_manager.install("nvm")

    elif isinstance(pkg_manager, WinGet):
        pkg_manager.install("Schniz.fnm")

    elif utils.is_unix() and not utils.is_installed("nvm"):
        url = "https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh"
        utils.shell.run(f"curl -o- {url} | bash")
        LOGGER.debug("Node was setup successfully.")
        return

    else:  # only on unix systems can there be no package manager
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")

    LOGGER.debug("Node was setup successfully.")
