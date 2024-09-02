"""Setup module containing a `setup` function for setting up Homebrew on a new
machine."""

import logging
import os

import config
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
    shell.run(cmd, throws=False)

    if machine_brewfile:  # install machine specific packages
        if not os.path.exists(machine_brewfile):
            raise utils.SetupError("Machine brewfile does not exist.")

        LOGGER.info("Installing machine specific packages...")
        cmd = f"{BREW} bundle --file={machine_brewfile}"
        shell.run(cmd, throws=False)

    # upgrade packages
    LOGGER.info("Upgrading packages...")
    shell.run(f"{BREW} upgrade", throws=False)

    # cleanup
    LOGGER.info("Cleaning up...")
    cmd = f"{BREW} cleanup --prune=all"
    shell.run(cmd, throws=False)
    LOGGER.info("Homebrew setup complete.")


def install_brew() -> None:
    """Install Homebrew on a new machine."""

    # update homebrew if it is already installed
    if BREW and os.path.exists(BREW):
        LOGGER.info("Updating Homebrew...")
        shell.run(f"{BREW} update")
    elif not BREW:  # check if homebrew is supported on the OS
        LOGGER.error("Homebrew is not supported on this OS.")
        return
    else:  # install homebrew otherwise
        LOGGER.info("Installing Homebrew...")
        cmd = '/bin/bash -c "$(curl -fsSL https://git.io/JIY6g)"'
        shell.run(cmd)

    # fix “zsh compinit: insecure directories” error
    shell.run(f'chmod -R go-w "$({BREW} --prefix)/share"')
    LOGGER.info("Fixed zsh `compinit` security error.")  # REVIEW: needed?


def is_installed() -> bool:
    """Check if Homebrew is installed on the machine."""
    return BREW is not None and os.path.exists(BREW)


if __name__ == "__main__":
    utils.PARSER.add_argument(
        "machine_brewfile",
        help="The path to the machine specific brewfile.",
        nargs="?",  # optional argument
        default=None,
    )
    args = utils.startup(description="Homebrew setup script.")
    utils.execute(setup, args.machine_brewfile)
