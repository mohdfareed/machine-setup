"""Library of modules containing setup methods used for setting up a new
machine. These methods are imported and used by the main `setup.py` script. The
modules in this library depend on modules in the `utils` library."""

import logging

import utils
from scripts.package_managers import *

LOGGER = logging.getLogger(__name__)
"""The package managers logger."""


def setup_docker(manager: PackageManager) -> None:
    """Setup docker on a new Debian machine."""
    LOGGER.info("Setting up Docker...")
    if isinstance(manager, HomeBrew):
        manager.install("docker", cask=True)
    elif isinstance(manager, WinGet):
        manager.install("Docker.DockerDesktop")
    else:  # use the official docker installation script
        utils.shell.run("curl -fsSL https://get.docker.com | sh")
    LOGGER.debug("Docker was setup successfully.")


def setup_python(manager: PackageManager) -> None:
    """Setup python on a new Debian machine."""
    LOGGER.info("Setting up Python...")
    if isinstance(manager, HomeBrew):
        manager.install("python pipx pyenv")
    if isinstance(manager, APT):
        manager.install("python3 python3-pip python3-venv pipx")
        utils.shell.run("curl https://pyenv.run | bash")
    if isinstance(manager, WinGet):
        manager.install("Python.Python")
        if not isinstance(manager, Scoop):
            LOGGER.warning(
                "Scoop is not installed. Skipping pipx and pyenv-win."
            )  # FIXME: this never happens, centralize managers
    LOGGER.debug("Python was setup successfully.")


def setup_node(manager: PackageManager) -> None:
    """Setup node on a new Debian machine."""
    LOGGER.info("Setting up Node...")
    if isinstance(manager, HomeBrew):
        manager.install("nvm")
    elif isinstance(manager, WinGet):
        manager.install("Schniz.fnm")
        utils.shell.run("fnm env --use-on-cd | Out-String | Invoke-Expression")
    elif utils.is_unix():
        url = "https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh"
        utils.shell.run(f"curl -o- {url} | bash")
    else:
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")
    LOGGER.debug("Node was setup successfully.")
