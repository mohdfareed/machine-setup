"""Utilities library containing modules and functions used within the project.
"""

import os

HOME: str = os.path.expanduser("~")
"""The home directory."""


def symlink(source: str, target: str) -> None:
    """Symlink a file from the source to the target. Overwrite the target if it
    already exists. The home directory is expanded for both the source and
    target.

    Args:
        source (str): The source file.
        target (str): The target file.
    """
    source = os.path.expanduser(source)
    target = os.path.expanduser(target)
    os.remove(target) if os.path.exists(target) else None
    os.symlink(source, target)
