"""Setup module containing a `setup` function for setting up the Snap store on
a new Debian machine."""

import logging

import utils
from scripts.package_managers import apt

LOGGER = logging.getLogger(__name__)
"""The snap setup logger."""


def setup() -> None:
    """Setup the snap store on a new Debian machine."""
    apt.validate()

    LOGGER.info("Setting up the snap store...")
    apt.install("snapd")
    install("snapd")
    LOGGER.debug("The snap store was setup successfully.")


def install(package: str, classic=False) -> None:
    """Install a snap store package."""
    validate()

    for pkg in package.split():
        LOGGER.info("Installing %s from the snap store...", pkg)
        utils.shell.run(
            f"sudo snap install {pkg} {'--classic' if classic else ''}"
        )
        LOGGER.debug("%s was installed successfully.", pkg)
    utils.shell.run("sudo snap refresh")


def validate() -> None:
    """Validate that the snap store is installed on the machine."""
    if not utils.is_installed("snap"):
        raise utils.SetupError(
            "The snap store is not installed on this machine."
        )


def try_install(package: str, classic=False) -> bool:
    """Try to install a package and return whether it was successful."""
    try:
        install(package, classic)
    except (utils.SetupError, utils.ShellError):
        return False
    return True


if __name__ == "__main__":
    args = utils.startup(description="The Snap store setup script.")
    utils.execute(setup)
