"""Setup module containing a `setup` function for setting up the Mac App Store
CLI on a new machine."""

__all__ = ["MAS"]

import os
from typing import Union

import utils
from scripts.package_managers.brew import HomeBrew
from scripts.package_managers.models import LOGGER, PackageManager
from utils import shell


class MAS(PackageManager):
    """Mac App Store."""

    mas = os.path.join(HomeBrew.bin, "mas")
    """The path to the mas executable."""

    def __init__(self, homebrew: HomeBrew) -> None:
        self.homebrew = homebrew
        """The Homebrew package manager."""
        super().__init__()

    @staticmethod
    def is_supported() -> bool:
        return utils.is_macos()

    @PackageManager.installation
    def install(self, package: Union[str, list[str]]) -> None:
        shell.execute(f"{self.mas} install {package}")

    def _setup(self) -> None:
        self.homebrew.install("mas")
        LOGGER.info("Updating Mac App Store applications...")
        shell.execute(f"{self.mas} upgrade")
