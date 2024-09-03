"""Setup module containing a `setup` function for setting up VSCode on a new
machine."""

import logging
import os

import config
import utils
from scripts import apt, brew
from utils import shell

LOGGER = logging.getLogger(__name__)
"""The VSCode setup logger."""


VSCODE: str | None = None
"""The path to the VSCode user settings directory."""

if utils.is_macos():
    VSCODE = os.path.join(
        os.path.expanduser("~"),
        "Library",
        "Application Support",
        "Code",
        "User",
    )
elif utils.is_linux():
    VSCODE = os.path.join(os.path.expanduser("~"), ".config", "Code", "User")
elif utils.is_windows():
    VSCODE = os.path.join(os.environ["APPDATA"], "Code", "User")


_config_files = ["settings.json", "keybindings.json", "snippets"]


def setup() -> None:
    """Setup VSCode on a new machine."""
    if not VSCODE:
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")
    install()

    LOGGER.info("Setting up VSCode...")
    for file in os.listdir(config.vscode):
        if file not in _config_files:
            continue
        utils.symlink_at(os.path.join(config.vscode, file), VSCODE)
    LOGGER.debug("VSCode was setup successfully.")


def install() -> None:
    """Install VSCode on a new machine."""

    LOGGER.info("Installing VSCode...")
    if utils.is_macos():
        brew.install("visual-studio-code")
    elif utils.is_linux():
        apt.install_snap("code", classic=True)
    elif utils.is_windows():
        LOGGER.info("Please install VSCode manually.")
    else:
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")
    LOGGER.debug("VSCode was installed successfully.")


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
    utils.execute(setup)
