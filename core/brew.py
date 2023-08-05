"""Setup module containing a `setup` function for setting up Homebrew on a new
machine."""

import os

import config
import utils

BIN = "/opt/homebrew/bin"
"""The path to the Homebrew executables."""
BREW = os.path.join(BIN, "brew")
"""The path to the brew executable."""

printer = utils.Printer("brew")
"""The Homebrew setup printer."""
shell = utils.Shell(printer.debug, printer.error, printer.logger.debug)
"""The Homebrew shell instance."""


def setup() -> None:
    """Setup Homebrew on a new machine by installing it and its packages."""
    printer.info("Setting up Homebrew...")
    install_brew()

    # install packages from Brewfile
    printer.print("Installing packages from Brewfile...")
    cmd = [BREW, "bundle", f"--file={config.brewfile}"]
    shell(cmd, silent=True, status="Installing...")
    printer.debug("Installed packages from Brewfile")

    # upgrade packages
    printer.print("Upgrading packages...")
    shell([BREW, "upgrade"], silent=True, status="Upgrading...")
    printer.debug("Upgraded packages")

    # upgrade mac app store packages
    printer.print("Upgrading mac app store packages...")
    mas = os.path.join(BIN, "mas")
    shell([mas, "upgrade"], silent=True, status="Upgrading...")
    printer.debug("Upgraded mac app store packages")

    # cleanup
    printer.print("Cleaning up...")
    cmd = [BREW, "cleanup", "--prune=all"]
    shell(cmd, silent=True, status="Cleaning up...")
    printer.success("Homebrew setup complete")


def install_brew():
    # update homebrew if it is already installed
    if os.path.exists(BREW):
        printer.print("Updating Homebrew...")
        shell([BREW, "update"], silent=True, status="Updating...")
        printer.success("Homebrew was updated")
    else:  # install homebrew otherwise
        printer.print("Installing Homebrew...")
        cmd = '/bin/bash -c "$(curl -fsSL https://git.io/JIY6g)"'
        shell(cmd, silent=True, status="Installing...")
        printer.success("Homebrew installed successfully")

    # fix “zsh compinit: insecure directories” error
    shell(f'chmod -R go-w "$({BREW} --prefix)/share"', silent=True)
    printer.debug("Fixed zsh `compinit` security error")  # TODO: fixed?
    # add fonts tap
    shell(f"{BREW} tap homebrew/cask-fonts", silent=True)
    printer.debug("Added Homebrew fonts tap")


if __name__ == "__main__":
    import argparse

    import core

    parser = argparse.ArgumentParser(description="Homebrew setup script.")
    args = parser.parse_args()
    core.run(setup, printer, "Failed to setup Homebrew")
