"""Helper functions for setting up the development environment."""

__all__ = [
    "SetupError",
    "machine_setup",
    "startup",
]

import argparse
import functools
import os
import sys
from typing import Any, Callable

from .filesystem import symlink
from .logging import LOGGER, setup_logging
from .shell import ShellError


class SetupError(Exception):
    """Exception due to a setup error."""


PARSER = argparse.ArgumentParser(
    description="Machine setup script.", formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
"""The command line argument parser."""


def startup() -> None:
    """Start the setup process for a machine."""
    PARSER.add_argument("-q", "--quiet", action="store_true", help="disable debug messages")
    PARSER.add_argument(
        "-m",
        "--private_machine",
        type=str,
        default=None,
        help="The path to a private machine configuration directory.",
    )

    # parse command-line arguments
    args = PARSER.parse_args()
    debug = not args.quiet
    private_machine = args.private_machine

    setup_logging(debug=debug)  # set up logging
    if private_machine:  # load private configuration
        _link_private_config(private_machine)


def machine_setup(setup_func: Callable[..., None]) -> Callable[..., None]:
    """Set up a machine by parsing command-line arguments, setting up logging, loading
    private configurations, and executing the setup function with error handling."""

    @functools.wraps(setup_func)
    def wrapper(*args: tuple[Any, ...], **kwargs: tuple[Any, ...]) -> None:
        LOGGER.info("Setting up machine...")
        _setup_machine(setup_func, *args, **kwargs)
        LOGGER.warning("Restart for some changes to apply.")
        LOGGER.info("Machine setup complete.")

    return wrapper


def _setup_machine(
    func: Callable[..., None], *args: tuple[Any, ...], **kwargs: tuple[Any, ...]
) -> None:
    """Execute a setup function with error handling."""
    try:
        func(*args, **kwargs)
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


def _link_private_config(private_machine: str) -> None:
    import config  # pylint: disable=import-outside-toplevel

    if not config.private_env or not config.ssh_keys:
        raise SetupError("Private machine not configured.")

    LOGGER.info("Loading private machine configuration: %s", private_machine)
    source_env = os.path.join(private_machine, os.path.basename(config.private_env))
    source_keys = os.path.join(private_machine, os.path.basename(config.ssh_keys))

    try:  # symlink private environment
        symlink(source_env, config.private_env)
    except FileNotFoundError:
        LOGGER.warning("Private environment not found.")

    try:  # symlink SSH keys
        symlink(source_keys, config.ssh_keys)
    except FileNotFoundError:
        LOGGER.warning("SSH keys not found.")
