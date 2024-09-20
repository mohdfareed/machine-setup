"""Package manager interface for installing and managing software packages."""

__all__ = ["PackageManager", "PackageManagerException"]

import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Union

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

    @staticmethod
    def installation(func: Callable[..., None]) -> Callable[..., None]:
        """Decorator to wrap installation process."""

        def wrapper(
            self: PackageManager, package: Union[str, list[str]], *args: Any, **kwargs: Any
        ) -> None:
            if isinstance(package, str):
                package = package.split()

            for pkg in package:
                LOGGER.info("Installing %s from %s...", pkg, self.name)
                func(self, pkg, *args, **kwargs)
                LOGGER.debug("%s was installed successfully.", pkg)

        return wrapper

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
