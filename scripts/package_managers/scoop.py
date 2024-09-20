"""Setup module containing a `setup` function for setting up Scoop on a new
Windows machine."""

__all__ = ["Scoop"]

from typing import override

import utils
from scripts.package_managers.models import LOGGER, PackageManager


class Scoop(PackageManager):
    """Scoop package manager."""

    @staticmethod
    def add_bucket(bucket: str) -> None:
        """Add a bucket to the scoop package manager."""
        LOGGER.info("Adding bucket %s to scoop...", bucket)
        utils.shell.run(f"scoop bucket add {bucket}", throws=False)
        LOGGER.debug("Bucket %s was added successfully.", bucket)

    @override
    @staticmethod
    def is_supported() -> bool:
        return utils.is_windows()

    @override
    def _install(self, package: str) -> None:
        utils.shell.run(f"scoop install {package}")

    @override
    def _setup(self) -> None:
        if not utils.is_installed("scoop"):  # install
            utils.shell.run("Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser")
            utils.shell.run('iex "& {$(irm get.scoop.sh)} -RunAsAdmin"')
        else:  # update
            utils.shell.run("scoop update")
            utils.shell.run("scoop update *")
