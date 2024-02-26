"""Setup module containing a `setup` function for setting up Git on a new
machine."""

import logging
import os

import config
from utils.shell import Shell

VSCODE = "$HOME/Library/Application Support/Code/User"
"""The path to the VSCode user settings directory."""

LOGGER = logging.getLogger(__name__)
"""The macOS setup logger."""
shell = Shell(LOGGER.debug, LOGGER.error)
"""The macOS shell instance."""


def setup() -> None:
    """Setup macOS on a new machine."""
    LOGGER.info("Setting up macOS...")

    # setup vscode settings
    LOGGER.info("Setting up VSCode...")
    os.makedirs(VSCODE, exist_ok=True)
    os.remove(os.path.join(VSCODE, "settings.json"))
    os.symlink(config.vscode_settings, os.path.join(VSCODE, "settings.json"))
    os.remove(os.path.join(VSCODE, "keybindings.json"))
    os.symlink(
        config.vscode_keybindings, os.path.join(VSCODE, "keybindings.json")
    )
    print.debug("Linked VSCode settings")

    # run the preferences script
    LOGGER.info("Setting system preferences...")
    shell(f". {config.macos_preferences}")


if __name__ == "__main__":
    import argparse

    import scripts

    parser = argparse.ArgumentParser(description="macOS setup script.")
    args = parser.parse_args()
    scripts.run(setup, LOGGER, "Failed to setup macOS")
