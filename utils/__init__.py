"""Utilities library containing modules and functions used within the project.
"""

import inspect as _inspect
import os as _os
import shutil as _shutil

from .printer import Printer

printer = Printer("utils")
"""Printer of the utils library."""


def abspath(*paths: str) -> str:
    """Get the absolute path of a file, eliminating symbolic links.

    Args:
        *paths (str): The path to resolve. If paths are given, they are joined.
    """
    return _os.path.realpath(_os.path.join(*paths))


def remove(path: str):
    """Remove a file, directory, or link at the given path.

    Args:
        path (str): The path to remove.
    """
    printer = _caller_printer()
    path = abspath(path)

    if _os.path.islink(path):
        _os.unlink(path)
        printer.debug(f"Unlinked: {path}")
    elif _os.path.isdir(path):
        _shutil.rmtree(path)
        printer.debug(f"Removed directory: {path}")
    elif _os.path.exists(path):
        _os.remove(path)
        printer.debug(f"Removed file: {path}")


def create_dir(directory: str, is_file=False):
    """Create a directory at the given path. If a file is provided, its parent
    is used as the directory.

    Args:
        directory (str): The path to the directory to create.
        is_file (bool, optional): Whether the directory is a file.
    """
    printer = _caller_printer()
    directory = abspath(directory)
    if is_file:  # use parent if file
        directory = _os.path.dirname(directory)

    # return if directory already exists
    if _os.path.isdir(directory):
        return
    elif _os.path.exists(directory):
        raise FileExistsError(f"Path exists: {directory}")

    # create directory if it doesn't exist
    _os.makedirs(directory, exist_ok=True)
    printer.debug(f"Created directory: {directory}")


def copy(source: str, target: str) -> None:
    """Copy a file from the source to the target. Overwrite the target if it
    already exists.

    Args:
        source (str): The source file.
        target (str): The target file.
    """
    printer = _caller_printer()

    # get absolute paths and check if source exists
    source, target = abspath(source), abspath(target)
    if not _os.path.exists(source):
        raise FileNotFoundError(f"File not found: {source}")

    remove(target)  # remove target if it exists
    create_dir(target, is_file=True)  # create parent
    _os.system(f"cp '{source}' '{target}'")  # create copy
    printer.debug(f"Copied: {source} -> {target}")


def symlink(source: str, target: str) -> None:
    """Symlink a file from the source to the target. Overwrite the target if it
    already exists.

    Args:
        source (str): The source file.
        target (str): The target file.
    """
    printer = _caller_printer()

    # get absolute paths and check if source exists
    source, target = _os.path.abspath(source), _os.path.abspath(target)
    if not _os.path.exists(source):
        raise FileNotFoundError(f"File not found: {source}")

    create_dir(target, is_file=True)  # create parent
    _os.system(f"ln -sf '{source}' '{target}'")  # create symlink
    printer.debug(f"Symlinked: {source} -> {target}")


def chmod(file: str, mode: int):
    """Change the permissions of a file.

    Args:
        file (str): The path to the file to change the permissions of.
        mode (int): The mode to change the permissions to.
    """
    printer = _caller_printer()
    file = abspath(file)
    _os.system(f"chmod {mode} '{file}'")
    printer.debug(f"Changed permissions: {file} -> {mode}")


def _caller_printer() -> Printer:
    # get the name of the calling module
    frame = _inspect.stack()[2]
    module = _inspect.getmodule(frame[0])
    return module.printer if hasattr(module, "printer") else printer
