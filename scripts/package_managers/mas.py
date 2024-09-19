"""Setup module containing a `setup` function for setting up the Mac App Store
CLI on a new machine."""

__all__ = ["MAS"]

import logging
from typing import Union, override

import utils
from scripts.package_managers import HomeBrew, PackageManager
from utils import shell

LOGGER = logging.getLogger(__name__)
"""The MAS package manager logger."""


class MAS(PackageManager):
    """Mac App Store."""

    mas: str
    """The path to the mas executable."""

    def __init__(self, homebrew: HomeBrew) -> None:
        self.homebrew = homebrew
        """The Homebrew package manager."""
        super().__init__()

    @override
    def install(self, package: Union[str, list[str]]) -> None:
        if isinstance(package, str):
            package = package.split()

        for pkg in package:
            LOGGER.info("Installing %s from the Mac App Store...", pkg)
            shell.run(f"{self.mas} install {pkg}")
            LOGGER.debug("%s was installed successfully.", pkg)
        shell.run(f"{self.homebrew.brew} cleanup --prune=all", throws=False)

    @override
    @staticmethod
    def is_supported() -> bool:
        return utils.is_macos()

    @override
    def _setup(self) -> None:
        LOGGER.info("Setting up the Mac App Store...")
        self.homebrew.install("mas")
        shell.run("mas upgrade")
        LOGGER.info("Mac App Store setup complete.")


if __name__ == "__main__":
    args = utils.startup(description="Mac App Store setup script.")
    utils.execute(MAS.__init__)
