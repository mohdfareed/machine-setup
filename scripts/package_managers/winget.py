"""Setup module containing a `setup` function for setting up WinGet on a new
Windows machine."""

__all__ = ["WinGet"]

from typing import override

import utils
from scripts.package_managers.models import PackageManager
from utils import shell


class WinGet(PackageManager):
    """WinGet package manager."""

    @override
    @staticmethod
    def is_supported() -> bool:
        return utils.is_installed("winget")

    @override
    def _install(self, package: str) -> None:
        shell.run(f"winget install -e --id {package}", throws=False)

    @override
    def _setup(self) -> None:
        shell.run("winget upgrade --all --include-unknown")
