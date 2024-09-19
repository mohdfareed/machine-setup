"""Setup module containing a `setup` function for setting up the Snap store on
a new Debian machine."""

__all__ = ["SnapStore"]

import logging
from typing import Union, override

import utils
from scripts.package_managers.apt import APT
from scripts.package_managers.models import PackageManager

LOGGER = logging.getLogger(__name__)
"""The Snap Store logger."""


class SnapStore(PackageManager):
    """Snap Store package manager."""

    def __init__(self, apt: APT) -> None:
        self.apt = apt
        """The Snap Store package manager."""
        super().__init__()

    @override
    def install(self, package: Union[str, list[str]], classic: bool = False) -> None:
        if isinstance(package, str):
            package = package.split()

        for pkg in package:
            LOGGER.info("Installing %s from the snap store...", pkg)
            utils.shell.run(f"sudo snap install {pkg} {'--classic' if classic else ''}")
            LOGGER.debug("%s was installed successfully.", pkg)
        utils.shell.run("sudo snap refresh")

    @override
    @staticmethod
    def is_supported() -> bool:
        return True

    @override
    def _setup(self) -> None:
        LOGGER.info("Setting up the snap store...")
        self.apt.install("snapd")
        self.install("snapd")
        LOGGER.debug("The snap store was setup successfully.")


if __name__ == "__main__":
    args = utils.startup(description="Snap Store setup script.")
    utils.execute(SnapStore.__init__)
