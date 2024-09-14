"""Setup module containing a `setup` function for setting up Tailscale on a new
machine."""

import logging
import os
import urllib.request

import utils
from scripts.package_managers import HomeBrew

LOGGER = logging.getLogger(__name__)
"""The tailscale setup logger."""


def setup(brew: HomeBrew | None) -> None:
    """Setup tailscale on a new machine."""
    LOGGER.info("Setting up tailscale...")

    if utils.is_macos() and brew:
        _setup_macos(brew)
    elif utils.is_linux():
        _setup_linux()
    elif utils.is_windows():
        _setup_windows()
    elif utils.is_macos():
        raise utils.SetupError("Homebrew is required for macOS.")
    else:
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")

    LOGGER.debug("Tailscale was setup successfully.")


def _setup_macos(brew: HomeBrew):
    brew.install("tailscale", cask=True)
    utils.shell.run("tailscale up", info=True)


def _setup_linux():
    if not utils.is_installed("tailscale"):
        utils.shell.run(
            "curl -fsSL https://tailscale.com/install.sh | sh", info=True
        )
    else:
        utils.shell.run("sudo tailscale update", info=True)
    utils.shell.run("sudo tailscale up", info=True)


def _setup_windows():
    if utils.is_installed("tailscale"):
        utils.shell.run("tailscale update", info=True)
        return

    installer_url = "https://pkgs.tailscale.com/stable/tailscale-setup.exe"
    installer_path = os.path.join(os.environ["TEMP"], "tailscale-setup.exe")
    urllib.request.urlretrieve(installer_url, installer_path)
    utils.shell.run(
        f"Start-Process -FilePath {installer_path} "
        "-ArgumentList '/quiet' -Wait",
        throws=False,
    )
    os.remove(installer_path)
    utils.shell.run("tailscale up", info=True)


if __name__ == "__main__":
    raise RuntimeError("This script is not meant to be run directly.")
