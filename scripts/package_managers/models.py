"""Package manager interface for installing and managing software packages."""

__all__ = ["PackageManager", "PackageManagerException"]

import logging
from abc import ABC, abstractmethod
from typing import Union

from utils import SetupError

LOGGER = logging.getLogger(__name__)
"""Package managers logger."""


class PackageManager(ABC):
    """Abstract base class for package managers."""

    @property
    def name(self) -> str:
        """The package manager name."""
        return self.__class__.__name__

    def __init__(self) -> None:
        if not self.is_supported():
            raise SetupError(f"Package manager {self.name} is not supported.")
        LOGGER.info("Setting up %s...", self.name)
        self._setup()
        LOGGER.debug("%s was setup successfully.", self.name)

    def install(self, package: Union[str, list[str]]) -> None:
        """Install a package."""
        if isinstance(package, str):
            package = package.split()

        for pkg in package:
            LOGGER.info("Installing %s from %s...", pkg, self.name)
            self._install(pkg)
            LOGGER.debug("%s was installed successfully.", pkg)

    @staticmethod
    @abstractmethod
    def is_supported() -> bool:
        """Check if the package manager is supported."""

    @abstractmethod
    def _install(self, package: str) -> None:
        """Install a package."""

    @abstractmethod
    def _setup(self) -> None:
        """Setup the package manager."""


class PackageManagerException(Exception):
    """Base exception for package manager errors."""
