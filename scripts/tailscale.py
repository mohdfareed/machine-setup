"""Setup module containing a `setup` function for setting up Tailscale on a new
machine."""

import logging
import os
import urllib.request

import utils
from scripts import brew

LOGGER = logging.getLogger(__name__)
"""The tailscale setup logger."""


def setup() -> None:
    """Setup tailscale on a new machine."""
    LOGGER.info("Setting up tailscale...")

    if utils.is_macos():
        setup_macos()
    elif utils.is_linux():
        setup_linux()
    elif utils.is_windows():
        setup_windows()
    else:
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")

    # start tailscale
    utils.shell.run("sudo tailscale up", info=True)
    LOGGER.debug("Tailscale was setup successfully.")


def setup_macos():
    """Setup Tailscale on macOS."""
    LOGGER.debug("Installing tailscale for macOS...")

    if brew.is_installed():
        utils.shell.run("brew install --cask tailscale")
    else:
        LOGGER.error("Homebrew is not installed. Skipping tailscale setup.")


def setup_linux():
    """Setup Tailscale on Linux."""
    LOGGER.debug("Installing tailscale for Linux...")
    utils.shell.run(
        "curl -fsSL https://tailscale.com/install.sh | sh", info=True
    )


def setup_windows():
    """Setup Tailscale on Windows."""
    LOGGER.debug("Installing tailscale for Windows...")
    installer_url = "https://pkgs.tailscale.com/stable/tailscale-setup.exe"
    installer_path = os.path.join(os.environ["TEMP"], "tailscale-setup.exe")

    urllib.request.urlretrieve(installer_url, installer_path)
    utils.shell.run(
        f"Start-Process -FilePath {installer_path} "
        "-ArgumentList '/quiet' -Wait",
        throws=False,
    )
    os.remove(installer_path)


if __name__ == "__main__":
    args = utils.startup(description="Tailscale setup script.")
    utils.execute(setup)
