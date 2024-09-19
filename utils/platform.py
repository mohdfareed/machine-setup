"""Platform specifications and utilities."""

__all__ = [
    "OS",
    "ARCH",
    "PLATFORM",
    "ARCHITECTURE",
    "UnsupportedOS",
    "is_macos",
    "is_linux",
    "is_unix",
    "is_windows",
    "is_arm",
]

import platform
from enum import Enum


class PLATFORM(Enum):
    """Enumeration of supported platforms."""

    LINUX = "Linux"
    MACOS = "Darwin"
    WINDOWS = "Windows"


class ARCHITECTURE(Enum):
    """Enumeration of supported architectures."""

    ARM = "arm"
    AMD = "64"


OS = PLATFORM(platform.system())
"""The current operating system."""
ARCH = ARCHITECTURE.ARM if "arm" in platform.machine() else ARCHITECTURE.AMD
"""The current architecture."""


def is_macos() -> bool:
    """Check if the current operating system is macOS."""
    return platform.system() == PLATFORM.MACOS.value


def is_linux() -> bool:
    """Check if the current operating system is Linux."""
    return platform.system() == PLATFORM.LINUX.value


def is_unix() -> bool:
    """Check if the current operating system is Unix."""
    return is_macos() or is_linux()


def is_windows() -> bool:
    """Check if the current operating system is Windows."""
    return platform.system() == PLATFORM.WINDOWS.value


def is_arm() -> bool:
    """Check if the current operating system is ARM based."""
    return str(ARCHITECTURE.ARM) in platform.machine()


class UnsupportedOS(Exception):
    """Exception due to an unsupported operating system."""
