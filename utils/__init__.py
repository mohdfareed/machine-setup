"""Utilities library containing modules and functions used within the project.
"""

import inspect as _inspect
import os as _os
import shutil as _shutil

from . import printer, shell
from .printer import Printer
from .shell import Shell

root_printer = printer.Printer("root")
"""The root printer."""


def abspath(*paths: str, resolve_links=True) -> str:
    """Get the absolute path of a file, eliminating symbolic links.

    Args:
        *paths (str): The path to resolve. If paths are given, they are joined.
    """
    combined_path = _os.path.join(*paths)
    expanded_path = _os.path.expanduser(combined_path)
    if not resolve_links:
        return _os.path.abspath(expanded_path)
    return _os.path.realpath(expanded_path)


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
    already exists. The target can be a directory, in which case the source
    is copied into the directory.

    Args:
        source (str): The source file.
        target (str): The target file or directory.
    """
    printer = _caller_printer()

    # copy directory if source is a directory
    if source.endswith("/"):
        copy_dir(source, target)
    if target.endswith("/"):  # copy into directory
        target = _os.path.join(target, _os.path.basename(source))

    # get absolute paths and check if source exists
    source, target = abspath(source), abspath(target)
    if not _os.path.exists(source):
        raise FileNotFoundError(f"File not found: {source}")

    remove(target)  # remove target if it exists
    create_dir(target, is_file=True)  # create parent
    _os.system(f"cp '{source}' '{target}' > /dev/null 2>&1")
    printer.debug(f"Copied: {_os.path.basename(source)} -> {target}")


def copy_dir(source: str, target: str) -> None:
    """Copy a directory from the source to the target. Overwrite the target if it
    already exists. The target can be a directory, in which case the source
    is copied into the directory.

    Args:
        source (str): The source directory.
        target (str): The target directory.
    """
    printer = _caller_printer()

    if target.endswith("/"):  # copy into directory
        target = _os.path.join(target, _os.path.basename(source))
    if source.endswith("/"):  # copy contents
        source = _os.path.join(source, "*")
    # preserve source wildcards
    target = abspath(target)

    create_dir(target, is_file=True)  # create parent
    _os.system(f"cp -R '{source}' '{target}' > /dev/null 2>&1")
    printer.debug(f"Copied: {_os.path.basename(source)} -> {target}")


def symlink(source: str, target: str) -> None:
    """Symlink a file from the source to the target. Overwrite the target if it
    already exists. The target can be a directory, in which case the source
    is symlinked into the directory.

    Args:
        source (str): The source file.
        target (str): The target file or directory.
    """
    printer = _caller_printer()

    if target.endswith("/"):  # symlink into directory
        target = _os.path.join(target, _os.path.basename(source))

    # get absolute paths and check if source exists
    source = abspath(source, resolve_links=False)
    target = abspath(target, resolve_links=False)
    if not _os.path.exists(source):
        raise FileNotFoundError(f"File not found: {source}")

    create_dir(target, is_file=True)  # create parent
    _os.system(f"ln -sf '{source}' '{target}'")  # create symlink
    printer.debug(f"Symlinked: {_os.path.basename(source)} -> {target}")


def chmod(file: str, mode: int):
    """Change the permissions of a file.

    Args:
        file (str): The path to the file to change the permissions of.
        mode (int): The mode to change the permissions to.
    """
    printer = _caller_printer()
    file = abspath(file)
    _os.system(f"chmod {mode} '{file}'")
    printer.debug(f"Changed permissions: {mode} => {file}")


def _caller_printer() -> printer.Printer:
    # get the name of the calling module
    frame = _inspect.stack()[2]
    module = _inspect.getmodule(frame[0])
    # return root printer if called from root
    if module.__name__ == __name__:
        return root_printer
    # return module printer if it exists
    return module.printer if hasattr(module, "printer") else root_printer
