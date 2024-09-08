"""Setup module containing a `setup` function for setting up Scoop on a new
Windows machine."""

import logging

import utils

LOGGER = logging.getLogger(__name__)
"""The scoop setup logger."""


def setup() -> None:
    """Setup the Scoop on a new Windows machine."""
    if not utils.is_windows():
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")

    LOGGER.info("Setting up Scoop...")
    utils.shell.run(
        "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
    )
    utils.shell.run(
        "Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression"
    )
    utils.shell.run("scoop update")
    utils.shell.run("scoop update *")
    LOGGER.debug("Scoop was setup successfully.")


def setup_fonts() -> None:
    """Setup fonts on a new machine."""
    validate()

    LOGGER.info("Setting up fonts...")
    install("nerd-fonts/JetBrains-Mono")
    LOGGER.debug("Fonts were setup successfully.")


def install(package: str) -> None:
    """Install a Scoop package."""
    validate()
    LOGGER.info("Installing %s with Scoop...", package)
    utils.shell.run(f"scoop install {package}")
    LOGGER.debug("%s was installed successfully.", package)


def validate() -> None:
    """Validate that Scoop is installed on the machine."""
    if not utils.is_installed("scoop"):
        raise utils.SetupError("Scoop is not installed on this machine.")


def try_install(package: str) -> bool:
    """Try to install a package and return whether it was successful."""
    try:
        install(package)
    except utils.SetupError:
        return False
    return True


if __name__ == "__main__":
    args = utils.startup(description="Scoop setup script.")
    utils.execute(setup)
