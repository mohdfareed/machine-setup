"""Setup module containing a `setup` function for setting up Homebrew on a new
machine."""

import logging
import os

import utils
from utils import shell

LOGGER = logging.getLogger(__name__)
"""The Homebrew setup logger."""

BIN: str | None = None
"""The path to the Homebrew executables."""

if utils.is_macos():
    BIN = os.path.join("/", "opt", "homebrew", "bin")
elif utils.is_linux():
    BIN = os.path.join("/", "home", "linuxbrew", ".linuxbrew", "bin")

BREW = os.path.join(BIN, "brew") if BIN else None
"""The path to the brew executable."""


def setup() -> None:
    """Setup Homebrew on a new machine by installing it and its packages."""
    if not BREW:  # check if homebrew is supported on the OS
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")

    LOGGER.info("Setting up Homebrew...")
    if not os.path.exists(BREW):
        _install_brew()
    shell.run(f"{BREW} update && {BREW} upgrade")
    LOGGER.info("Homebrew setup complete.")


def setup_fonts() -> None:
    """Setup fonts on a new machine."""
    validate()

    LOGGER.info("Setting up fonts...")
    install("font-computer-modern")
    install("font-jetbrains-mono-nerd-font")
    LOGGER.debug("Fonts were setup successfully.")


def install(package: str, cask=False) -> None:
    """Install a Homebrew package."""
    validate()

    LOGGER.info("Installing %s from Homebrew...", package)
    shell.run(f"{BREW} install {'--cask' if cask else ''} {package}")
    shell.run(f"{BREW} cleanup --prune=all", throws=False)
    LOGGER.debug("%s was installed successfully.", package)


def install_brewfile(file: str) -> None:
    """Install Homebrew packages from a Brewfile."""
    validate()

    LOGGER.info("Installing Homebrew packages from Brewfile...")
    shell.run(f"{BREW} bundle install --file={file}")
    shell.run(f"{BREW} cleanup --prune=all", throws=False)
    LOGGER.debug("Homebrew packages were installed successfully.")


def validate() -> None:
    """Validate the Homebrew setup."""
    if BREW is None or not os.path.exists(BREW):
        raise utils.SetupError("Homebrew is not installed on this machine.")


def try_install(package: str, cask=False) -> bool:
    """Try to install a package and return whether it was successful."""
    try:
        install(package, cask)
    except utils.SetupError:
        return False
    return True


def _install_brew() -> None:
    """Install Homebrew on a new machine."""
    LOGGER.info("Installing Homebrew...")
    try:  # install homebrew otherwise
        shell.run('/bin/bash -c "$(curl -fsSL https://git.io/JIY6g)"')
    except shell.ShellError as ex:
        raise utils.SetupError("Failed to install Homebrew.") from ex

    # fix “zsh compinit: insecure directories” error
    shell.run(f'chmod -R go-w "$({BREW} --prefix)/share"')
    LOGGER.info("Fixed zsh `compinit` security error.")  # REVIEW: needed?


if __name__ == "__main__":
    args = utils.startup(description="Homebrew setup script.")
    utils.execute(setup)
