"""Setup module containing a `setup` function for setting up the Mac App Store
CLI on a new machine."""

__all__ = ["MAS"]

import os
from typing import Union, override

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

    @override
    @staticmethod
    def is_supported() -> bool:
        return utils.is_macos()

    @override
    @PackageManager.installation
    def install(self, package: Union[str, list[str]]) -> None:
        shell.run(f"{self.mas} install {package}")

    @override
    def _setup(self) -> None:
        self.homebrew.install("mas")
        LOGGER.info("Updating Mac App Store applications...")
        shell.run("mas upgrade")
