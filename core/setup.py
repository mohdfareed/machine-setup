"""Helper functions for setting up the development environment."""

__all__ = [
    "SetupError",
    "machine_setup",
]

import argparse
import functools
import inspect
import logging
import os
import sys
from typing import Any, Callable

import utils

LOGGER = logging.getLogger(__name__)
"""The machine setup logger."""


def machine_setup(setup_func: Callable[..., None]) -> Callable[..., None]:
    """Machine setup decorator."""

    # create argument parser
    machine = setup_func.__module__
    parser = argparse.ArgumentParser(
        description=f"{machine} setup script.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # add private machine argument
    parser.add_argument(
        "-m",
        "--private_machine",
        type=str,
        default=None,
        help="The path to a private machine configuration directory.",
    )

    # create arguments parser
    parser = _parse_cli_args(setup_func, parser)
    args = _startup(parser)

    # setup private configuration
    if args.private_machine:
        _link_private_config(args.private_machine)

    # start the setup process
    @functools.wraps(setup_func)
    def wrapper() -> None:
        LOGGER.info("Setting up %s...", machine)
        _setup_machine(setup_func, args)
        LOGGER.warning("Restart for some changes to apply.")
        LOGGER.info("Machine setup complete.")

    return wrapper


def _startup(parser: argparse.ArgumentParser) -> argparse.Namespace:
    # ensure quiet flag is not already set
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="disable debug messages"
    )

    # parse command-line arguments
    args = parser.parse_args()
    debug = not args.quiet

    # setup logging
    utils.setup_logging(debug=debug)

    # return args without quiet flag
    return args


def _setup_machine(func: Callable[..., None], *args: Any) -> None:
    """Execute a setup function with error handling."""
    try:
        func(*args)
    except KeyboardInterrupt:
        print()
        LOGGER.warning("Setup interrupted.")
        sys.exit(0)

    except (SetupError, utils.ShellError) as exception:
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
        utils.symlink(source_env, config.private_env)
    except FileNotFoundError:
        LOGGER.warning("Private environment not found.")

    try:  # symlink SSH keys
        utils.symlink(source_keys, config.ssh_keys)
    except FileNotFoundError:
        LOGGER.warning("SSH keys not found.")


def _parse_cli_args(
    func: Callable[..., None], parser: argparse.ArgumentParser
) -> argparse.ArgumentParser:
    sig = inspect.signature(func)
    for name, param in sig.parameters.items():

        # check if boolean argument (flags)
        if param.annotation == bool:
            parser.add_argument(
                f"--{name}",
                action="store_true",
                help=param.__doc__,
            )
            continue

        # parse argument
        if param.default == inspect.Parameter.empty:
            arg_name = name
            required = True
        else:
            arg_name = f"--{name}"
            required = False

        parser.add_argument(
            arg_name,
            required=required,
            default=None if required else param.default,
            help=param.__doc__,
        )
    return parser


class SetupError(Exception):
    """Exception due to a setup error."""
