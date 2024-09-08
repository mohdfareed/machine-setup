"""Library of modules containing setup methods used for setting up a new
machine. These methods are imported and used by the main `setup.py` script. The
modules in this library depend on modules in the `utils` library."""

import logging

import utils
from scripts.package_managers import *  # import all package managers

LOGGER = logging.getLogger(__name__)
"""The package managers logger."""


def setup_docker() -> None:
    """Setup docker on a new Debian machine."""
    LOGGER.info("Setting up Docker...")
    if brew.try_install("docker", cask=True):
        pass
    elif winget.try_install("Docker.DockerDesktop"):
        pass
    else:  # use the official docker installation script
        utils.shell.run("curl -fsSL https://get.docker.com | sh")
    LOGGER.debug("Docker was setup successfully.")


def setup_python() -> None:
    """Setup python on a new Debian machine."""
    LOGGER.info("Setting up Python...")

    if brew.try_install("python pipx pyenv"):
        pass
    elif apt.try_install("python3 python3-pip python3-venv pipx"):
        utils.shell.run("curl https://pyenv.run | bash")
    elif winget.try_install("Python.Python"):
        if not scoop.try_install("pipx pyenv-win"):
            LOGGER.warning(
                "Scoop is not installed. Skipping pipx and pyenv-win."
            )
    LOGGER.debug("Python was setup successfully.")


def setup_node() -> None:
    """Setup node on a new Debian machine."""
    LOGGER.info("Setting up Node...")
    if brew.try_install("nvm"):
        pass
    elif winget.try_install("Schniz.fnm"):
        utils.shell.run("fnm env --use-on-cd | Out-String | Invoke-Expression")
    elif utils.is_unix():
        url = "https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh"
        utils.shell.run(f"curl -o- {url} | bash")
    else:
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")
    LOGGER.debug("Node was setup successfully.")
