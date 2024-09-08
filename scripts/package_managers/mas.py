"""Setup module containing a `setup` function for setting up MAS on a new
machine."""

import logging
import os

import utils
from scripts.package_managers import brew
from utils import shell

LOGGER = logging.getLogger(__name__)
"""The MAS setup logger."""

MAS = os.path.join(brew.BIN, "mas") if brew.BIN else None
"""The path to the mas executable."""


def setup() -> None:
    """Setup Homebrew on a new machine by installing it and its packages."""
    if not utils.is_macos():
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")
    brew.validate()

    LOGGER.info("Setting up the Mac App Store...")
    brew.install("mas")
    shell.run("mas upgrade")
    LOGGER.info("Mac App Store setup complete.")


def install(package: str) -> None:
    """Install a Mac App Store package."""
    validate()
    for pkg in package.split():
        LOGGER.info("Installing %s from the Mac App Store...", pkg)
        shell.run(f"{MAS} install {pkg}")
        LOGGER.debug("%s was installed successfully.", pkg)


def validate() -> None:
    """Validate that MAS is installed on the machine."""
    if MAS is None or not os.path.exists(MAS):
        raise utils.SetupError("MAS is not installed on this machine.")


def try_install(package: str) -> bool:
    """Try to install a package and return whether it was successful."""
    try:
        install(package)
    except utils.SetupError:
        return False
    return True


if __name__ == "__main__":
    args = utils.startup(description="Homebrew setup script.")
    utils.execute(setup)
