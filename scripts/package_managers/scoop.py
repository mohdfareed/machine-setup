"""Setup module containing a `setup` function for setting up Scoop on a new
Windows machine."""

__all__ = ["Scoop"]

import logging
from typing import Union, override

import utils
from scripts.package_managers.models import PackageManager

LOGGER = logging.getLogger(__name__)
"""Scoop package manager logger."""


class Scoop(PackageManager):
    """Scoop package manager."""

    def setup_fonts(self) -> None:
        """Setup fonts on a new machine."""
        LOGGER.info("Setting up fonts...")
        self.add_bucket("nerd-fonts")
        self.install("nerd-fonts/JetBrains-Mono")
        LOGGER.debug("Fonts were setup successfully.")

    @staticmethod
    def add_bucket(bucket: str) -> None:
        """Add a bucket to the scoop package manager."""
        LOGGER.info("Adding bucket %s to scoop...", bucket)
        utils.shell.run(f"scoop bucket add {bucket}", throws=False)
        LOGGER.debug("Bucket %s was added successfully.", bucket)

    @override
    def install(self, package: Union[str, list[str]]) -> None:
        if isinstance(package, str):
            package = package.split()

        for pkg in package:
            LOGGER.info("Installing %s with Scoop...", pkg)
            utils.shell.run(f"scoop install {pkg}")
            LOGGER.debug("%s was installed successfully.", pkg)

    @override
    @staticmethod
    def is_supported() -> bool:
        return utils.is_windows()

    @override
    def _setup(self) -> None:
        LOGGER.info("Setting up Scoop...")

        # install
        if not utils.is_installed("scoop"):
            utils.shell.run("Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser")
            utils.shell.run('iex "& {$(irm get.scoop.sh)} -RunAsAdmin"')
        else:
            # update
            utils.shell.run("scoop update")
            utils.shell.run("scoop update *")
        LOGGER.debug("Scoop was setup successfully.")


if __name__ == "__main__":
    args = utils.startup(description="Scoop setup script.")
    utils.execute(Scoop.__init__)
