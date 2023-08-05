"""Setup module containing a `setup` function for setting up Homebrew on a new
machine."""

import config
import utils

printer = utils.Printer("brew")
"""The Homebrew setup printer."""
shell = utils.Shell(printer.debug, printer.error)
"""The Homebrew shell instance."""


def setup() -> None:
    """Setup Homebrew on a new machine by installing it and its packages."""
    printer.info("Setting up Homebrew...")

    install_brew()
    configure_brew()

    # install packages from Brewfile
    printer.print("Installing packages from Brewfile...")
    cmd = f"--file={config.brewfile}"
    if shell(["brew", "bundle", cmd], status="Installing packages...") != 0:
        raise RuntimeError("Failed to install packages from Brewfile.")
    printer.debug("Installed packages from Brewfile")

    # upgrade packages
    printer.print("Upgrading packages...")
    if shell(["brew", "upgrade"], status="Upgrading packages...") != 0:
        raise RuntimeError("Failed to upgrade packages.")
    printer.debug("Upgraded packages")
    printer.print("Upgrading mac app store packages...")
    if shell(["mas", "upgrade"], status="Upgrading App Store apps...") != 0:
        raise RuntimeError("Failed to upgrade App Store apps.")
    printer.debug("Upgraded mac app store packages")

    # cleanup
    printer.print("Cleaning up...")
    if shell(["brew", "cleanup"], status="Cleaning up...") != 0:
        raise RuntimeError("Failed to cleanup.")
    printer.success("Homebrew setup complete")


def install_brew():
    """Run the Homebrew installation script."""
    # check if homebrew is already installed
    if shell(["command", "-v", "brew"], silent=True)[1] == 0:
        printer.debug("Homebrew is already installed")

        # update homebrew if it is already installed
        printer.print("Updating Homebrew...")
        if shell(["brew", "update"], status="Updating Homebrew...") != 0:
            raise RuntimeError("Failed to update Homebrew")
        return printer.success("Homebrew was updated")

    # install homebrew otherwise
    printer.print("Installing Homebrew...")
    cmd = '/bin/bash -c "$(curl -fsSL https://git.io/JIY6g)"'
    if shell(cmd, status="Installing Homebrew...") != 0:
        raise RuntimeError("Failed to install Homebrew")
    printer.success("Homebrew installed successfully")


def configure_brew():
    # add homebrew to path
    if shell('eval "$(/opt/homebrew/bin/brew shellenv)"', silent=True)[1] != 0:
        raise RuntimeError("An error occurred while loading Homebrew.")
    printer.debug("Loaded Homebrew")

    # fix “zsh compinit: insecure directories” error
    if shell('chmod -R go-w "$(brew --prefix)/share"', silent=True)[1] != 0:
        raise RuntimeError("Failed to fix zsh `compinit` message.")
    printer.debug("Fixed zsh `compinit` security error")  # TODO: fixed?

    # add fonts tap
    if shell("brew tap homebrew/cask-fonts") != 0:
        raise RuntimeError("Failed to add fonts tap.")
    printer.debug("Added Homebrew fonts tap")


if __name__ == "__main__":
    import argparse

    import core

    parser = argparse.ArgumentParser(description="Homebrew setup script.")
    args = parser.parse_args()
    core.run(setup, printer, "Failed to setup Homebrew")
