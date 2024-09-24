"""Setup module containing a `setup` function for setting up Scoop on a new
Windows machine."""

__all__ = ["Scoop"]

from typing import Union

import utils
from scripts.package_managers.models import LOGGER, PackageManager


class Scoop(PackageManager):
    """Scoop package manager."""

    @staticmethod
    def add_bucket(bucket: str) -> None:
        """Add a bucket to the scoop package manager."""
        LOGGER.info("Adding bucket %s to scoop...", bucket)
        utils.shell.execute(f"scoop bucket add {bucket}", throws=False)
        LOGGER.debug("Bucket %s was added successfully.", bucket)

    @staticmethod
    def is_supported() -> bool:
        return utils.is_windows()

    @PackageManager.installation
    def install(self, package: Union[str, list[str]]) -> None:
        utils.shell.execute(f"scoop install {package}")

    def _setup(self) -> None:
        if not utils.is_installed("scoop"):  # install
            utils.shell.execute(
                "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
            )
            utils.shell.execute('iex "& {$(irm get.scoop.sh)} -RunAsAdmin"')
        else:  # update
            utils.shell.execute("scoop update")
            utils.shell.execute("scoop update *")
