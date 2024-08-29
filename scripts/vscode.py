"""Setup module containing a `setup` function for setting up VSCode on a new
machine."""

import logging
import os

import config
import utils
from utils import shell

LOGGER = logging.getLogger(__name__)
"""The VSCode setup logger."""

_ignored_files = [".DS_Store"]

VSCODE: str
"""The path to the VSCode user settings directory."""

if utils.is_macos():
    VSCODE = "~/Library/Application Support/Code/User"
elif utils.is_linux():
    VSCODE = "~/.config/Code/User"
elif utils.is_windows():
    VSCODE = "%APPDATA%\\Code\\User"
else:
    raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")


def setup() -> None:
    """Setup VSCode on a new machine."""

    LOGGER.info("Setting up VSCode...")
    for file in os.listdir(config.vscode):
        if file in _ignored_files:
            continue
        utils.symlink_at(os.path.join(config.vscode, file), VSCODE)
    LOGGER.debug("VSCode was setup successfully.")


def setup_tunnels() -> None:
    """Setup VSCode SSH tunnels as a service."""

    LOGGER.info("Setting up VSCode SSH tunnels...")

    vscode = shell.run("which code")[1].strip()
    cmd = (
        f"{vscode} tunnel service install "
        "--accept-server-license-terms --name rpi"
    )
    shell.run(cmd, info=True)

    LOGGER.debug("VSCode SSH tunnels were setup successfully.")


if __name__ == "__main__":
    args = utils.startup(description="VSCode setup script.")
    utils.execute(setup, args.vscode_settings)
