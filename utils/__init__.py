"""Utilities library containing modules and functions used within the project.
"""

import os
import platform
from enum import Enum

from .logging import LOGGER, setup_logging
from .shell import run


class PLATFORM(Enum):
    """Enumeration of supported platforms."""

    LINUX = "Linux"
    MACOS = "Darwin"
    WINDOWS = "Windows"


def load_env_var(zshenv_path: str, var_name: str) -> str:
    """Load the environment variable value."""
    command = f"source {zshenv_path} && echo ${var_name}"
    return run(command)[1]


def symlink(src: str, dst: str) -> None:
    """Create a symbolic link from `src` to `dst`. If the destination exists,
    it will be overwritten. If the destination's directory structure does not
    exist, it will be created."""
    dst = os.path.expanduser(dst)
    src = os.path.expanduser(src)
    is_dir = os.path.isdir(src)

    try:  # remove existing file
        os.remove(dst)
    except FileNotFoundError:
        pass

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    os.symlink(src, dst, target_is_directory=is_dir)
    LOGGER.debug("Linked {%s} -> {%s}", src, dst)


def symlink_at(src: str, dst_dir: str) -> None:
    """Create a symbolic link from 'src' to 'dst_dir/src'. If the destination
    exists, it will be overwritten. If the destination's directory structure
    does not exist, it will be created."""
    dst = os.path.join(os.path.expanduser(dst_dir), os.path.basename(src))
    symlink(src, dst)


def is_macos() -> bool:
    """Check if the current operating system is macOS."""

    return platform.system() == PLATFORM.MACOS


def is_linux() -> bool:
    """Check if the current operating system is Linux."""

    return platform.system() == PLATFORM.LINUX


def is_windows() -> bool:
    """Check if the current operating system is Windows."""

    return platform.system() == PLATFORM.WINDOWS
