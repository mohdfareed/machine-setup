"""Setup module containing a `setup` function for setting up VSCode on a new
machine."""

import logging

import config
import utils

VSCODE: str
"""The path to the VSCode user settings directory."""

if utils.is_macos():
    VSCODE = "~/Library/Application Support/Code/User"
if utils.is_linux():
    VSCODE = "~/.config/Code/User"
if utils.is_windows():
    VSCODE = "%APPDATA%\\Code\\User"
else:
    raise utils.UnsupportedOS("Unsupported operating system.")


LOGGER = logging.getLogger(__name__)
"""The git setup logger."""


def setup() -> None:
    """Setup git on a new machine."""
    LOGGER.info("Setting up VSCode...")

    utils.symlink_at(config.vscode_settings, VSCODE)
    utils.symlink_at(config.vscode_keybindings, VSCODE)
    utils.symlink_at(config.vscode_snippets, VSCODE)
    LOGGER.debug("Git was setup successfully.")


if __name__ == "__main__":
    args = utils.startup(description="Git setup script.")
    utils.execute(setup)
