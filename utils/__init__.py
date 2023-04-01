"""Utilities library containing modules and functions used within the project.
"""

import os as _os


def symlink(source: str, target: str) -> None:
    """Symlink a file from the source to the target. Overwrite the target if it
    already exists. The home directory is expanded for both the source and
    target.

    Args:
        source (str): The source file.
        target (str): The target file.
    """
    # get absolute paths and check if source exists
    source, target = abs_path(source), abs_path(target)
    if not _os.path.exists(source):
        raise FileNotFoundError(f"File not found: {source}")

    _os.makedirs(_os.path.dirname(target), exist_ok=True)    # create structure
    _os.unlink(target) if _os.path.exists(target) else None  # overwrite
    _os.symlink(source, target)                              # create symlink


def copy(source: str, target: str) -> None:
    """Copy a file from the source to the target. Overwrite the target if it
    already exists. The home directory is expanded for both the source and
    target.

    Args:
        source (str): The source file.
        target (str): The target file.
    """
    # get absolute paths and check if source exists
    source, target = abs_path(source), abs_path(target)
    if not _os.path.exists(source):
        raise FileNotFoundError(f"File not found: {source}")

    _os.makedirs(_os.path.dirname(target), exist_ok=True)    # create structure
    _os.remove(target) if _os.path.exists(target) else None  # overwrite
    _os.system(f"cp '{source}' '{target}'")                  # create copy


def create_file(file: str, overwrite: bool = False):
    """Create a file at the given path. The home directory is expanded for the
    given path.

    Args:
        file (str): The path to the file to create.
    """
    file = abs_path(file)
    if overwrite:                                        # overwrite
        _os.remove(file) if _os.path.exists(file) else None
    _os.makedirs(_os.path.dirname(file), exist_ok=True)  # create structure
    _os.system(f"touch '{file}'")                          # create file


def create_dir(directory: str):
    """Create a directory at the given path. The home directory is expanded for
    the given path.

    Args:
        directory (str): The path to the directory to create.
    """
    directory = abs_path(directory)
    _os.makedirs(directory, exist_ok=True)  # create directory


def remove(path: str):
    """Remove a file or directory at the given path. The home directory is
    expanded for the given path.

    Args:
        path (str): The path to the file or directory to remove.
    """
    path = abs_path(path)
    _os.remove(path) if _os.path.exists(path) else None  # remove file


def abs_path(path: str) -> str:
    """Returns the absolute path of the given path. The home directory is
    expanded for the given path.

    Args:
        path (str): The path to expand.

    Returns:
        str: The absolute path.
    """
    return _os.path.abspath(_os.path.expanduser(path))
