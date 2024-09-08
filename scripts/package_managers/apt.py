"""Setup module containing a `setup` function for setting up APT on a on a new
Debian machine."""

import logging

import utils

LOGGER = logging.getLogger(__name__)
"""The apt setup logger."""


def setup() -> None:
    """Setup apt on a new Debian machine."""
    validate()

    LOGGER.info("Setting up Debian apt...")
    utils.shell.run("sudo apt update && sudo apt upgrade -y")
    LOGGER.debug("Debian apt was setup successfully.")


def install(package: str) -> None:
    """Install an apt package."""
    validate()

    LOGGER.info("Installing %s from apt...", package)
    utils.shell.run(f"sudo apt install -y {package}")
    utils.shell.run("sudo apt autoremove -y")
    LOGGER.debug("%s was installed successfully.", package)


def validate() -> None:
    """Validate that manager's environment."""
    if not utils.is_installed("apt"):
        raise utils.SetupError("APT is not installed on this machine.")


def try_install(package: str) -> bool:
    """Try to install a package and return whether it was successful."""
    try:
        install(package)
    except utils.SetupError:
        return False
    return True


if __name__ == "__main__":
    args = utils.startup(description="APT setup script.")
    utils.execute(setup)
