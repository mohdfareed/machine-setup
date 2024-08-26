"""Utilities library containing modules and functions used within the project.
"""

import argparse as _argparse
import os as _os
import platform as _platform
import sys as _sys
from collections.abc import Callable as _Callable
from enum import Enum as _Enum

from utils.shell import ShellError

from .logging import LOGGER
from .logging import setup_logging as _setup_logging
from .shell import run as _run

# MARK - Platform


class UnsupportedOS(Exception):
    """Exception due to an unsupported operating system."""


class PLATFORM(_Enum):
    """Enumeration of supported platforms."""

    LINUX = "Linux"
    MACOS = "Darwin"
    WINDOWS = "Windows"


def is_macos() -> bool:
    """Check if the current operating system is macOS."""

    return _platform.system() == PLATFORM.MACOS.value


def is_linux() -> bool:
    """Check if the current operating system is Linux."""

    return _platform.system() == PLATFORM.LINUX.value


def is_windows() -> bool:
    """Check if the current operating system is Windows."""

    return _platform.system() == PLATFORM.WINDOWS.value


# MARK - Setup

PARSER = _argparse.ArgumentParser(
    prog="machine-setup",
    description="Setup the machine.",
    epilog="REPO: github.com/mohdfareed/machine",
    formatter_class=_argparse.ArgumentDefaultsHelpFormatter,
)
"""The command line argument parser."""


class SetupError(Exception):
    """Exception due to a setup error."""


def startup(
    setup: str | None = None,
    description: str | None = None,
) -> _argparse.Namespace:
    """Parse command line arguments and setup logging."""

    if setup:
        PARSER.set_defaults(setup=setup)
    if description:
        PARSER.description = description

    PARSER.add_argument(
        "-d", "--debug", action="store_true", help="print debug messages"
    )
    args = PARSER.parse_args()
    execute(_setup_logging, debug=args.debug)  # type: ignore
    return args


def execute(setup: _Callable, *args, **kwargs) -> None:
    """Execute a setup method with logging and error handling."""

    try:
        setup(*args, **kwargs)
    except KeyboardInterrupt:
        print()
        LOGGER.warning("Setup interrupted.")
        _sys.exit(0)
    except (SetupError, ShellError) as exception:
        LOGGER.exception(exception)
        LOGGER.error("Setup failed.")
        _sys.exit(1)
    except Exception as exception:  # pylint: disable=broad-except
        LOGGER.exception(exception)
        LOGGER.error("An unexpected error occurred.")
        _sys.exit(1)


# MARK - File System


def load_env_var(zshenv_path: str, var_name: str) -> str:
    """Load the environment variable value."""
    command = f"source '{zshenv_path}' && echo ${var_name}"
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
