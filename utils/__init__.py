"""Utilities library containing modules and functions used within the project.
"""

import os

from .logging import setup_logging
from .shell import run as run_cmd
from .shell import setup_sudo

LOGGER = logging.logging.getLogger(__name__)
"""The utils logger."""


def is_macos() -> bool:
    """Check if the current operating system is macOS."""
    import platform

    return platform.system() == "Darwin"


def symlink(src: str, dst: str, is_dir=False) -> None:
    """Create a symbolic link from `src` to `dst`. If the destination exists,
    it will be removed. If the destination's parent directory does not exist,
    it will be created. If the destination is a directory, the link will be
    created inside it."""

    dst = os.path.expanduser(dst)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isdir(dst):  # create link inside directory
        dst = os.path.join(dst, os.path.basename(src))
    if os.path.exists(dst) or os.path.islink(dst):
        os.remove(dst)  # remove existing file or link
    os.symlink(src, dst, target_is_directory=is_dir)
    LOGGER.debug(f"Linked {src} -> {dst}")
