"""Setup module containing a `setup` function for setting up VSCode on a new
machine."""

import logging

import config
import utils
from utils import shell

LOGGER = logging.getLogger(__name__)
"""The VSCode setup logger."""

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
    for file in config.vscode:
        utils.symlink_at(file, VSCODE)
    LOGGER.debug("VSCode was setup successfully.")


def setup_tunnels() -> None:
    """Setup VSCode SSH tunnels on a new machine."""

    LOGGER.info("Setting up VSCode SSH tunnels...")

    vscode = shell.run(["which", "code"])[1].strip()
    cmd = (
        f"{vscode} tunnel service install "
        "--accept-server-license-terms --name rpi"
    ).split()
    shell.run(cmd, msg="Installing VSCode SSH tunnels")

    LOGGER.debug("VSCode SSH tunnels were setup successfully.")


if __name__ == "__main__":
    args = utils.startup(description="VSCode setup script.")
    utils.execute(setup, args.vscode_settings)
