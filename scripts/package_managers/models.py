"""Package manager interface for installing and managing software packages."""

__all__ = ["PackageManager", "PackageManagerException"]

from abc import ABC, abstractmethod
from typing import Union

from utils import SetupError


class PackageManager(ABC):
    """Abstract base class for package managers."""

    def __init__(self) -> None:
        if not self.is_supported():
            raise SetupError("Package manager is not supported.")
        self._setup()

    @abstractmethod
    def install(self, package: Union[str, list[str]]) -> None:
        """Install a package."""

    @staticmethod
    @abstractmethod
    def is_supported() -> bool:
        """Check if the package manager is supported."""

    @abstractmethod
    def _setup(self) -> None:
        """Setup the package manager."""


class PackageManagerException(Exception):
    """Base exception for package manager errors."""
