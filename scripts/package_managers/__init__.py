"""Package managers for installing and managing software packages."""

from abc import ABC as _ABC
from abc import abstractmethod as _abstractmethod

from utils import SetupError as _SetupError


class PackageManager(_ABC):
    """Abstract base class for package managers."""

    def __init__(self) -> None:
        if not self.is_supported():
            raise _SetupError("Package manager is not supported.")
        self._setup()

    @_abstractmethod
    def install(self, package: str | list[str]) -> None:
        """Install a package."""

    @staticmethod
    @_abstractmethod
    def is_supported() -> bool:
        """Check if the package manager is supported."""

    @_abstractmethod
    def _setup(self) -> None:
        """Setup the package manager."""


class PackageManagerException(Exception):
    """Base exception for package manager errors."""


# import all package managers.

from .apt import APT  # pylint: disable=wrong-import-position
from .brew import HomeBrew  # pylint: disable=wrong-import-position
from .mas import MAS  # pylint: disable=wrong-import-position
from .scoop import Scoop  # pylint: disable=wrong-import-position
from .snap import SnapStore  # pylint: disable=wrong-import-position
from .winget import WinGet  # pylint: disable=wrong-import-position
