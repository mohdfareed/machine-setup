"""Utilities library containing modules and functions used within the project.
"""

import argparse as _argparse
import os as _os
import platform as _platform
import sys as _sys
from collections.abc import Callable as _Callable
from enum import Enum as _Enum

from .logging import LOGGER
from .logging import setup_logging as _setup_logging
from .shell import _EXECUTABLE, ShellError
from .shell import run as _run

# MARK - Platform =============================================================


class UnsupportedOS(Exception):
    """Exception due to an unsupported operating system."""


class PLATFORM(_Enum):
    """Enumeration of supported platforms."""

    LINUX = "Linux"
    MACOS = "Darwin"
    WINDOWS = "Windows"


class ARCHITECTURE(_Enum):
    """Enumeration of supported architectures."""

    ARM = "arm"
    AMD = "64"

    @staticmethod
    def current() -> str:
        """Return the current architecture."""
        return str(ARCHITECTURE.ARM) if is_arm() else str(ARCHITECTURE.AMD)


def is_macos() -> bool:
    """Check if the current operating system is macOS."""

    return _platform.system() == PLATFORM.MACOS.value


def is_linux() -> bool:
    """Check if the current operating system is Linux."""

    return _platform.system() == PLATFORM.LINUX.value


def is_unix() -> bool:
    """Check if the current operating system is Unix."""

    return is_macos() or is_linux()


def is_windows() -> bool:
    """Check if the current operating system is Windows."""

    return _platform.system() == PLATFORM.WINDOWS.value


def is_arm() -> bool:
    """Check if the current operating system is ARM based."""
    return str(ARCHITECTURE.ARM) in _platform.machine()


OS = PLATFORM(_platform.system())
"""The current operating system."""

ARCH = ARCHITECTURE.ARM if is_arm() else ARCHITECTURE.AMD
"""The current architecture."""

# MARK - Setup ================================================================

PARSER = _argparse.ArgumentParser(
    description="Machine setup script.",
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
        "-q", "--quiet", action="store_true", help="disable debug messages"
    )  # default to logging debug messages
    args = PARSER.parse_args()
    execute(_setup_logging, debug=not args.quiet)  # type: ignore
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


# MARK - File System ==========================================================


def load_env_var(env_path: str, var_name: str) -> str:
    """Load the environment variable value.
    On Windows, the environment variable is loaded using PowerShell. On Unix,
    the environment variable is loaded using the Z shell."""
    if is_windows():
        ps_command = f"$env:{var_name}"
        command = (
            f"{_EXECUTABLE} -NoProfile -File {env_path} -EnvOnly {ps_command}"
        )
    else:
        command = f"source '{env_path}' && echo ${var_name}"
    return _run(command)[1]


def symlink(src: str, dst: str) -> None:
    """Create a symbolic link from `src` to `dst`. If the destination exists,
    it will be overwritten. If the destination's directory structure does not
    exist, it will be created."""
    dst = _os.path.expanduser(dst)
    src = _os.path.expanduser(src)
    is_dir = _os.path.isdir(src)

    if is_windows():
        _run(f"Remove-Item -Recurse -Force '{dst}'", throws=False)
    else:
        _run(f"sudo rm -rf '{dst}'", throws=False)
    _os.makedirs(_os.path.dirname(dst), exist_ok=True)
    _os.symlink(src, dst, target_is_directory=is_dir)
    LOGGER.debug("Linked '%s' -> '%s'", src, dst)


def symlink_at(src: str, dst_dir: str) -> None:
    """Create a symbolic link from 'src' to 'dst_dir/src'. If the destination
    exists, it will be overwritten. If the destination's directory structure
    does not exist, it will be created."""
    dst = _os.path.join(_os.path.expanduser(dst_dir), _os.path.basename(src))
    symlink(src, dst)


def is_installed(command: str) -> bool:
    """Check if a command is installed."""
    if is_windows():
        return (
            _run(
                f"Get-Command {command} -ErrorAction SilentlyContinue",
                throws=False,
            )[0]
            == 0
        )
    return _run(f"command -v {command}", throws=False)[0] == 0
