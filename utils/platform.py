"""Platform specifications and utilities."""

__all__ = [
    "OS",
    "ARCH",
    "Unsupported",
    "is_macos",
    "is_linux",
    "is_unix",
    "is_windows",
    "is_arm",
]

import platform
from enum import Enum


class _PLATFORM(Enum):
    LINUX = "Linux"
    MACOS = "Darwin"
    WINDOWS = "Windows"


class _ARCHITECTURE(Enum):
    ARM = "arm"
    AMD = "64"


OS = _PLATFORM(platform.system())
"""The current operating system."""
ARCH = _ARCHITECTURE.ARM if "arm" in platform.machine() else _ARCHITECTURE.AMD
"""The current architecture."""


def is_windows() -> bool:
    """Check if the current operating system is Windows."""
    return platform.system() == _PLATFORM.WINDOWS.value


def is_macos() -> bool:
    """Check if the current operating system is macOS."""
    return platform.system() == _PLATFORM.MACOS.value


def is_linux() -> bool:
    """Check if the current operating system is Linux."""
    return platform.system() == _PLATFORM.LINUX.value


def is_unix() -> bool:
    """Check if the current operating system is Unix."""
    return is_macos() or is_linux()


def is_arm() -> bool:
    """Check if the current operating system is ARM based."""
    return str(_ARCHITECTURE.ARM) in platform.machine()


class Unsupported(Exception):
    """Exception due to an unsupported machine configuration."""
