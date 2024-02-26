"""Utilities library containing modules and functions used within the project.
"""

import os
import shutil

from .logging import setup_logging
from .shell import run as run_shell

LOGGER = logging.logging.getLogger(__name__)
"""The utils logger."""


def is_macos() -> bool:
    """Check if the current operating system is macOS."""
    import platform

    return platform.system() == "Darwin"


def is_installed(executable: str) -> bool:
    """Check if an executable is installed."""
    import os

    return os.path.exists(executable)


def symlink(src: str, dst: str, is_dir=False) -> None:
    """Create a symbolic link from `src` to `dst`. If the destination exists,
    it will be removed. If the destination's parent directory does not exist,
    it will be created. If the destination is a directory, the link will be
    created inside it."""

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isdir(dst):  # create link inside directory
        dst = os.path.join(dst, os.path.basename(src))
    if os.path.exists(dst) or os.path.islink(dst):
        os.remove(dst)  # remove existing file or link
    os.symlink(src, dst, target_is_directory=is_dir)
    LOGGER.debug(f"Linked {src} -> {dst}")


# def delete(path: str):
#     """Delete a file, directory, or link at the given path.
#     Args:
#         path (str): The path to remove.
#     """
#     path = os.path.abspath(path)

#     if os.path.islink(path):
#         os.unlink(path)
#     elif os.path.isdir(path):
#         shutil.rmtree(path)
#     elif os.path.exists(path):
#         os.remove(path)
#     LOGGER.debug(f"Deleted {path}")
