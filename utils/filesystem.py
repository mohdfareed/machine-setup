"""Filesystem helper utilities."""

__all__ = [
    "delete",
    "is_installed",
    "load_env_var",
    "symlink",
    "symlink_at",
]
import os
import pathlib
import shutil

from .logging import LOGGER
from .platform import is_windows
from .shell import EXECUTABLE, SupportedExecutables, run


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
    """Create a symbolic link from `src` to `dst`. Overwrites the
    destination. Creates the destination structure."""
    dst = os.path.expanduser(dst)
    src = os.path.expanduser(src)

    if is_windows():
        delete(dst)
    else:
        run(f"sudo rm -rf '{dst}'", throws=False)

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    os.symlink(src, dst, target_is_directory=os.path.isdir(src))
    LOGGER.debug("Linked '%s' -> '%s'", src, dst)


def symlink_at(src: str, dst_dir: str) -> None:
    """Create a symbolic link from 'src' to 'dst_dir/src'. Overwrites the
    destination. Creates the destination structure."""
    symlink(src, os.path.join(os.path.expanduser(dst_dir), os.path.basename(src)))


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
        return run(f"Get-Command {command} -ErrorAction SilentlyContinue", throws=False)[0] == 0
    return run(f"command -v {command}", throws=False)[0] == 0
