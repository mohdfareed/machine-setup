"""Setup module containing a `setup` function for setting up the Snap store on
a new Debian machine."""

__all__ = ["SnapStore"]

from typing import Union

import utils
from scripts.package_managers.apt import APT
from scripts.package_managers.models import PackageManager


class SnapStore(PackageManager):
    """Snap Store package manager."""

    def __init__(self, apt: APT) -> None:
        self.apt = apt
        """The Snap Store package manager."""
        super().__init__()

    @PackageManager.installation
    def install(self, package: Union[str, list[str]], classic: bool = False) -> None:
        utils.shell.run(f"sudo snap install {package} {'--classic' if classic else ''}")

    @staticmethod
    def is_supported() -> bool:
        return True

    def _setup(self) -> None:
        self.apt.install("snapd")
        self.install("snapd")
