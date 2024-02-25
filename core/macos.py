"""Setup module containing a `setup` function for setting up Git on a new
machine."""

import config
import utils

VSCODE = "$HOME/Library/Application Support/Code/User"
"""The path to the VSCode user settings directory."""

printer = utils.Printer("macos")
"""The macOS setup printer."""
shell = utils.Shell(printer.debug, printer.error)
"""The macOS shell instance."""


def setup() -> None:
    """Setup macOS on a new machine."""
    printer.info("Setting up macOS...")

    # setup vscode settings
    printer.print("Setting up VSCode...")
    utils.symlink(config.vscode_settings, VSCODE)
    utils.symlink(config.vscode_keybindings, VSCODE)
    print.debug("Linked VSCode settings")

    # run the preferences script
    printer.print("Setting system preferences...")
    shell(f". {config.macos_preferences}")


if __name__ == "__main__":
    import argparse

    import core

    parser = argparse.ArgumentParser(description="macOS setup script.")
    args = parser.parse_args()
    core.run(setup, printer, "Failed to setup macOS")
