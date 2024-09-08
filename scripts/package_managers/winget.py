"""Setup module containing a `setup` function for setting up WinGet on a new
Windows machine."""

import logging

import utils
from utils import shell

LOGGER = logging.getLogger(__name__)
"""The WinGet setup logger."""


def setup() -> None:
    """Setup WinGet on a new Windows machine."""
    if not utils.is_windows():
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")
    validate()

    LOGGER.info("Setting up WinGet...")
    shell.run("winget install -e --id Microsoft.Powershell")
    shell.run("winget install -e --id Microsoft.Git")
    LOGGER.debug("WinGet was setup successfully.")


def install(package: str) -> None:
    """Install a winget package."""
    validate()

    for pkg in package.split():
        LOGGER.info("Installing %s from winget...", pkg)
        shell.run(f"winget install -e --id {pkg}")
        LOGGER.debug("%s was installed successfully.", pkg)


def try_install(package: str) -> bool:
    """Try to install a package and return whether it was successful."""
    try:
        install(package)
    except utils.SetupError:
        return False
    return True


def validate() -> None:
    """Validate that winget is installed on the machine."""
    if not utils.is_installed("winget"):
        raise utils.SetupError("WinGet is not installed on this machine.")


if __name__ == "__main__":
    args = utils.startup(description="WinGet setup script.")
    utils.execute(setup)
