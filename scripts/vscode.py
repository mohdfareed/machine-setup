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


def setup(vscode_settings=VSCODE) -> None:
    """Setup git on a new machine."""
    LOGGER.info("Setting up VSCode...")

    for file in config.vscode:
        utils.symlink_at(file, vscode_settings)
    LOGGER.debug("VSCode was setup successfully.")


if __name__ == "__main__":
    utils.PARSER.add_argument(
        "vscode_settings",
        help="The path to the VSCode user settings directory.",
        nargs="?",
        default=VSCODE,
    )
    args = utils.startup(description="VSCode setup script.")
    utils.execute(setup, args.vscode_settings)
