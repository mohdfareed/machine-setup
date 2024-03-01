"""Setup module containing a `setup` function for setting up Git on a new
machine."""

import logging

import config
import utils

VSCODE = "~/Library/Application Support/Code/User"
"""The path to the VSCode user settings directory on macOS."""

LOGGER = logging.getLogger(__name__)
"""The macOS setup logger."""


def setup() -> None:
    """Setup macOS on a new machine."""
    LOGGER.info("Setting up macOS...")

    # setup vscode settings
    LOGGER.info("Setting up VSCode...")
    utils.symlink(config.vscode_settings, VSCODE)
    utils.symlink(config.vscode_keybindings, VSCODE)
    LOGGER.debug("Linked VSCode settings.")

    # setup npm config
    utils.symlink(config.npm_config_userconfig, config.npmrc)
    # run the preferences script
    LOGGER.info("Setting system preferences...")
    # utils.run_cmd(f". {config.macos_preferences}")
    LOGGER.debug("System preferences set.")

    LOGGER.info("macOS setup complete.")


if __name__ == "__main__":
    import argparse

    import scripts

    parser = argparse.ArgumentParser(description="macOS setup script.")
    args = parser.parse_args()
    scripts.run_setup_isolated(setup)
