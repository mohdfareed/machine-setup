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
MAS = os.path.join(BIN, "mas") if BIN else None
"""The path to the mas executable."""


def setup() -> None:
    """Setup Homebrew on a new machine by installing it and its packages."""
    LOGGER.info("Setting up Homebrew...")
    install_brew()
    install(f"zsh git git-lfs gh nvim {'mas' if utils.is_macos() else ''}")
    update()
    LOGGER.info("Homebrew setup complete.")


def install_brew() -> None:
    """Install Homebrew on a new machine."""

    if not BREW:  # check if homebrew is supported on the OS
        LOGGER.error("Homebrew is not supported on this OS.")
        return

    # brew already exists
    if os.path.exists(BREW):
        return

    LOGGER.info("Installing Homebrew...")
    try:  # install homebrew otherwise
        shell.run('/bin/bash -c "$(curl -fsSL https://git.io/JIY6g)"')
    except shell.ShellError as ex:
        raise utils.SetupError("Failed to install Homebrew.") from ex

    # fix “zsh compinit: insecure directories” error
    shell.run(f'chmod -R go-w "$({BREW} --prefix)/share"')
    LOGGER.info("Fixed zsh `compinit` security error.")  # REVIEW: needed?


def update() -> None:
    """Update Homebrew and its packages."""
    LOGGER.info("Updating Homebrew...")
    shell.run(f"{BREW} update && {BREW} upgrade")
    if utils.is_macos():
        shell.run(f"{MAS} upgrade")
    LOGGER.info("Homebrew was updated successfully.")


def install(package: str, cask=False) -> None:
    """Install a Homebrew package."""
    LOGGER.info("Installing %s from Homebrew...", package)
    shell.run(f"{BREW} install {'--cask' if cask else ''} {package}")
    shell.run(f"{BREW} cleanup --prune=all", throws=False)
    LOGGER.debug("%s was installed successfully.", package)


def install_mas(package: str) -> None:
    """Install a Mac App Store package."""
    if not utils.is_macos():
        raise utils.UnsupportedOS("Mac App Store is only supported on macOS.")

    LOGGER.info("Installing %s from the Mac App Store...", package)
    shell.run(f"{MAS} install {package}")
    LOGGER.debug("%s was installed successfully.", package)


def install_brewfile(file: str) -> None:
    """Install Homebrew packages from a Brewfile."""
    LOGGER.info("Installing Homebrew packages from Brewfile...")
    shell.run(f"{BREW} bundle install --file={file}")
    LOGGER.debug("Homebrew packages were installed successfully.")


def setup_python() -> None:
    """Setup python on a new Debian machine."""
    LOGGER.info("Setting up Python...")
    install("python pipx pyenv pyenv-virtualenv")
    LOGGER.debug("Python was setup successfully.")


def setup_node() -> None:
    """Setup node on a new Debian machine."""
    LOGGER.info("Setting up Node...")
    install("node nvm")
    LOGGER.debug("Node was setup successfully.")


def setup_fonts() -> None:
    """Setup fonts on a new machine."""
    LOGGER.info("Setting up fonts...")
    install("font-computer-modern")
    install("font-jetbrains-mono-nerd-font")
    LOGGER.debug("Fonts were setup successfully.")


def is_installed() -> bool:
    """Check if Homebrew is installed on the machine."""
    return utils.is_installed("brew")


def is_mas_installed() -> bool:
    """Check if Mac App Store is installed on the machine."""
    return utils.is_installed("mas")


if __name__ == "__main__":
    args = utils.startup(description="Homebrew setup script.")
    utils.execute(setup)
