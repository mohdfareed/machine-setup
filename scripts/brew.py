"""Setup module containing a `setup` function for setting up Homebrew on a new
machine."""

import logging
import os

import config
import utils
from utils import shell

LOGGER = logging.getLogger(__name__)
"""The Homebrew setup logger."""

BIN: str
"""The path to the Homebrew executables."""

if utils.is_macos():
    BIN = "/opt/homebrew/bin"
elif utils.is_linux():
    BIN = "/home/linuxbrew/.linuxbrew/bin"
else:
    raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")

BREW = os.path.join(BIN, "brew")
"""The path to the brew executable."""
MAS = os.path.join(BIN, "mas")
"""The path to the mas executable."""


def setup(machine_brewfile: str | None = None) -> None:
    """Setup Homebrew on a new machine by installing it and its packages."""
    LOGGER.info("Setting up Homebrew...")

    try:  # install homebrew
        install_brew()
    except shell.ShellError as ex:
        raise utils.SetupError("Failed to install Homebrew.") from ex

    # install brew and core packages
    LOGGER.info("Installing core packages...")
    cmd = f"{BREW} bundle --file={config.brewfile}"
    shell.run(cmd, msg="Installing packages", throws=False)

    if machine_brewfile:  # install machine specific packages
        if not os.path.exists(machine_brewfile):
            LOGGER.error("Machine brewfile does not exist.")
            return

        LOGGER.info("Installing machine specific packages...")
        cmd = f"{BREW} bundle --file={machine_brewfile}"
        shell.run(cmd, msg="Installing packages", throws=False)

    # upgrade packages
    LOGGER.info("Upgrading packages...")
    shell.run(f"{BREW} upgrade", msg="Upgrading packages", throws=False)

    # cleanup
    LOGGER.info("Cleaning up...")
    cmd = f"{BREW} cleanup --prune=all"
    shell.run(cmd, msg="Cleaning up", throws=False)
    LOGGER.info("Homebrew setup complete.")


def install_brew() -> None:
    """Install Homebrew on a new machine."""

    # update homebrew if it is already installed
    if os.path.exists(BREW):
        shell.run(f"{BREW} update", msg="Updating brew")
        LOGGER.info("Homebrew was updated.")

    else:  # install homebrew otherwise
        LOGGER.info("Installing Homebrew...")
        cmd = '/bin/bash -c "$(curl -fsSL https://git.io/JIY6g)"'
        shell.run(cmd, msg="Installing brew")
        LOGGER.info("Homebrew installed successfully.")

    # fix “zsh compinit: insecure directories” error
    shell.run(f'chmod -R go-w "$({BREW} --prefix)/share"')
    LOGGER.info("Fixed zsh `compinit` security error.")  # REVIEW: needed?


if __name__ == "__main__":
    utils.PARSER.add_argument(
        "machine_brewfile",
        help="The path to the machine specific brewfile.",
        nargs="?",
        default=None,
    )
    args = utils.startup(description="Homebrew setup script.")
    utils.execute(setup, args.machine_brewfile)
