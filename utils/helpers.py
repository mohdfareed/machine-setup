"""Utilities library containing modules and functions used within the project.
"""

import os as _os
import platform as _platform
from enum import Enum as _Enum

from .logging import LOGGER
from .shell import run as _run


class PLATFORM(_Enum):
    """Enumeration of supported platforms."""

    LINUX = "Linux"
    MACOS = "Darwin"
    WINDOWS = "Windows"


def load_env_var(zshenv_path: str, var_name: str) -> str:
    """Load the environment variable value."""
    command = f"source {zshenv_path} && echo ${var_name}"
    return _run(command)[1]


def symlink(src: str, dst: str) -> None:
    """Create a symbolic link from `src` to `dst`. If the destination exists,
    it will be overwritten. If the destination's directory structure does not
    exist, it will be created."""
    dst = _os.path.expanduser(dst)
    src = _os.path.expanduser(src)
    is_dir = _os.path.isdir(src)

    try:  # remove existing file
        _os.remove(dst)
    except FileNotFoundError:
        pass

    _os.makedirs(_os.path.dirname(dst), exist_ok=True)
    _os.symlink(src, dst, target_is_directory=is_dir)
    LOGGER.debug("Linked \\[%s] -> \\[%s]", src, dst)


def symlink_at(src: str, dst_dir: str) -> None:
    """Create a symbolic link from 'src' to 'dst_dir/src'. If the destination
    exists, it will be overwritten. If the destination's directory structure
    does not exist, it will be created."""
    dst = _os.path.join(_os.path.expanduser(dst_dir), _os.path.basename(src))
    symlink(src, dst)


def is_macos() -> bool:
    """Check if the current operating system is macOS."""

    return _platform.system() == PLATFORM.MACOS.value


def is_linux() -> bool:
    """Check if the current operating system is Linux."""

    return _platform.system() == PLATFORM.LINUX.value


def is_windows() -> bool:
    """Check if the current operating system is Windows."""

    return _platform.system() == PLATFORM.WINDOWS.value
