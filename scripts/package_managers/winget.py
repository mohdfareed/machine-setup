"""Setup module containing a `setup` function for setting up WinGet on a new
Windows machine."""

import logging
from typing import override

import utils
from scripts.package_managers import PackageManager
from utils import shell

LOGGER = logging.getLogger(__name__)
"""WinGet package manager logger."""


class WinGet(PackageManager):
    """WinGet package manager."""

    @override
    def install(self, package: str | list[str]) -> None:
        if isinstance(package, str):
            package = package.split()

        for pkg in package:
            LOGGER.info("Installing %s from winget...", pkg)
            shell.run(f"winget install -e --id {pkg}", throws=False)
            LOGGER.debug("%s was installed successfully.", pkg)

    @override
    @staticmethod
    def is_supported() -> bool:
        return utils.is_windows() and utils.is_installed("winget")

    @override
    def _setup(self) -> None:
        LOGGER.info("Setting up WinGet...")
        shell.run("winget upgrade --all --include-unknown")
        LOGGER.debug("Scoop was setup successfully.")


if __name__ == "__main__":
    args = utils.startup(description="WinGet setup script.")
    utils.execute(WinGet)
