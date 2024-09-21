"""Setup module containing a `setup` function for setting up Tailscale on a new machine."""

__all__ = ["setup"]

import logging
import os
import urllib.request
from typing import Optional

import utils
from scripts.package_managers import HomeBrew

LOGGER = logging.getLogger(__name__)
"""The tailscale setup logger."""


def setup(brew: Optional[HomeBrew]) -> None:
    """Setup tailscale on a new machine."""
    LOGGER.info("Setting up tailscale...")
    if brew:
        brew.install("tailscale", cask=True)

    elif utils.is_linux():
        if not utils.is_installed("tailscale"):
            utils.shell.run("curl -fsSL https://tailscale.com/install.sh | sh", info=True)

    elif utils.is_windows():
        installer_url = "https://pkgs.tailscale.com/stable/tailscale-setup.exe"
        installer_path = os.path.join(os.environ["TEMP"], "tailscale-setup.exe")
        urllib.request.urlretrieve(installer_url, installer_path)
        utils.shell.run(
            f"Start-Process -FilePath {installer_path} -ArgumentList '/quiet' -Wait", throws=False
        )
        os.remove(installer_path)

    else:
        raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")
    utils.shell.run("sudo tailscale update", info=True)
    LOGGER.debug("Tailscale was setup successfully.")
