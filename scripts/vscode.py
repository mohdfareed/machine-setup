"""Setup module containing a `setup` function for setting up VSCode on a new
machine."""

import logging
import os

import config
import utils
from scripts import brew, snap, winget
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

    LOGGER.info("Setting up VSCode...")
    _install()
    for file in os.listdir(config.vscode):
        if file not in _config_files:
            continue
        utils.symlink_at(os.path.join(config.vscode, file), VSCODE)
    LOGGER.debug("VSCode was setup successfully.")


def setup_tunnels(name: str) -> None:
    """Setup VSCode SSH tunnels as a service."""
    if not utils.is_installed("code"):
        raise utils.SetupError("VSCode is not installed on this machine.")

    LOGGER.info("Setting up VSCode SSH tunnels...")
    cmd = (
        f"code tunnel service install "
        f"--accept-server-license-terms --name {name}"
    )
    shell.run(cmd, info=True)
    LOGGER.debug("VSCode SSH tunnels were setup successfully.")


def _install():
    if not (
        brew.try_install("visual-studio-code")
        or winget.try_install("Microsoft.VisualStudioCode")
        or snap.try_install("code", classic=True)
    ):
        raise utils.SetupError(
            "Could not install VSCode. Please install it manually."
        )


if __name__ == "__main__":
    args = utils.startup(description="VSCode setup script.")
    utils.execute(setup)
