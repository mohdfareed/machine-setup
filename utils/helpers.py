"""Helper functions for setting up the development environment."""

__all__ = [
    "ARCH",
    "ARCHITECTURE",
    "OS",
    "PLATFORM",
    "PARSER",
    "SetupError",
    "UnsupportedOS",
    "delete",
    "execute",
    "is_arm",
    "is_linux",
    "is_macos",
    "is_unix",
    "is_windows",
    "is_installed",
    "load_env_var",
    "startup",
    "symlink",
    "symlink_at",
]

import argparse
import os
import pathlib
import platform
import shutil
import sys
from collections.abc import Callable
from enum import Enum
from typing import Any, Optional

from .logging import LOGGER, setup_logging
from .shell import EXECUTABLE, ShellError, SupportedExecutables, run

# MARK - Platform =============================================================


class UnsupportedOS(Exception):
    """Exception due to an unsupported operating system."""


class PLATFORM(Enum):
    """Enumeration of supported platforms."""

    LINUX = "Linux"
    MACOS = "Darwin"
    WINDOWS = "Windows"


class ARCHITECTURE(Enum):
    """Enumeration of supported architectures."""

    ARM = "arm"
    AMD = "64"

    @staticmethod
    def current() -> str:
        """Return the current architecture."""
        return str(ARCHITECTURE.ARM) if is_arm() else str(ARCHITECTURE.AMD)


def is_macos() -> bool:
    """Check if the current operating system is macOS."""

    return platform.system() == PLATFORM.MACOS.value


def is_linux() -> bool:
    """Check if the current operating system is Linux."""

    return platform.system() == PLATFORM.LINUX.value


def is_unix() -> bool:
    """Check if the current operating system is Unix."""

    return is_macos() or is_linux()


def is_windows() -> bool:
    """Check if the current operating system is Windows."""

    return platform.system() == PLATFORM.WINDOWS.value


def is_arm() -> bool:
    """Check if the current operating system is ARM based."""
    return str(ARCHITECTURE.ARM) in platform.machine()


OS = PLATFORM(platform.system())
"""The current operating system."""

ARCH = ARCHITECTURE.ARM if is_arm() else ARCHITECTURE.AMD
"""The current architecture."""

# MARK - Setup ================================================================

PARSER = argparse.ArgumentParser(
    description="Machine setup script.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
"""The command line argument parser."""


class SetupError(Exception):
    """Exception due to a setup error."""


def startup(
    setup: Optional[str] = None,
    description: Optional[str] = None,
) -> argparse.Namespace:
    """Parse command line arguments and setup logging."""

    if setup:
        PARSER.set_defaults(setup=setup)
    if description:
        PARSER.description = description

    PARSER.add_argument(
        "-q", "--quiet", action="store_true", help="disable debug messages"
    )  # default to logging debug messages
    args = PARSER.parse_args()
    execute(setup_logging, debug=not args.quiet)  # type: ignore
    return args


def execute(
    setup: Callable[..., None],
    *args: tuple[Any, ...],
    **kwargs: dict[str, Any],
) -> None:
    """Execute a setup method with logging and error handling."""

    try:
        setup(*args, **kwargs)
    except KeyboardInterrupt:
        print()
        LOGGER.warning("Setup interrupted.")
        sys.exit(0)
    except (SetupError, ShellError) as exception:
        LOGGER.exception(exception)
        LOGGER.error("Setup failed.")
        sys.exit(1)
    except Exception as exception:  # pylint: disable=broad-except
        LOGGER.exception(exception)
        LOGGER.error("An unexpected error occurred.")
        sys.exit(1)


# MARK - File System ==========================================================


def load_env_var(env_path: str, var_name: str) -> str:
    """Load the environment variable value.
    On Windows, the environment variable is loaded using PowerShell. On Unix,
    the environment variable is loaded using the Z shell."""
    command = (
        f"& '{env_path}' -EnvOnly; Write-Output $env:{var_name}"
        if is_windows()
        else f"source '{env_path}' && echo ${var_name}"
    )
    return run(command)[1]


def symlink(src: str, dst: str) -> None:
    """Create a symbolic link from `src` to `dst`. If the destination exists,
    it will be overwritten. If the destination's directory structure does not
    exist, it will be created."""
    dst = os.path.expanduser(dst)
    src = os.path.expanduser(src)
    is_dir = os.path.isdir(src)

    if is_windows():
        delete(dst)
    else:
        run(f"sudo rm -rf '{dst}'", throws=False)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    os.symlink(src, dst, target_is_directory=is_dir)
    LOGGER.debug("Linked '%s' -> '%s'", src, dst)


def symlink_at(src: str, dst_dir: str) -> None:
    """Create a symbolic link from 'src' to 'dst_dir/src'. If the destination
    exists, it will be overwritten. If the destination's directory structure
    does not exist, it will be created."""
    dst = os.path.join(os.path.expanduser(dst_dir), os.path.basename(src))
    symlink(src, dst)


def delete(path: str) -> None:
    """Delete a file or directory at the specified path."""
    item = pathlib.Path(path)
    if not item.exists():
        return

    if item.is_symlink() or item.is_file():
        item.unlink()
    if item.is_dir():
        shutil.rmtree(item)
    LOGGER.debug("Deleted: %s", path)


def is_installed(command: str) -> bool:
    """Check if a command is installed."""
    if EXECUTABLE == SupportedExecutables.PWSH_WIN:
        return (
            run(
                f"Get-Command {command} -ErrorAction SilentlyContinue",
                throws=False,
            )[0]
            == 0
        )
    return run(f"command -v {command}", throws=False)[0] == 0
