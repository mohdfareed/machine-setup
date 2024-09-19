"""Setup module containing a `setup` function for setting up fonts on a new machine."""

__all__ = ["setup"]

import logging
from typing import Union

from scripts.package_managers import APT, HomeBrew, Scoop

LOGGER = logging.getLogger(__name__)
"""The fonts setup logger."""


def setup(pkg_manager: Union[HomeBrew, APT, Scoop]) -> None:
    """Setup fonts on a new machine."""
    LOGGER.info("Setting up tailscale...")
    if isinstance(pkg_manager, HomeBrew):
        pkg_manager.install("font-computer-modern font-jetbrains-mono-nerd-font")
    elif isinstance(pkg_manager, APT):
        pkg_manager.install("fonts-jetbrains-mono fonts-lmodern")
    else:
        pkg_manager.add_bucket("nerd-fonts")
        pkg_manager.install("nerd-fonts/JetBrains-Mono")
    LOGGER.debug("Fonts were setup successfully.")


if __name__ == "__main__":
    raise RuntimeError("This script is not meant to be run directly.")
