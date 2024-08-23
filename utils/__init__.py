"""Helper functions that wraps setup execution with error handling and logging.
"""

import argparse as _argparse
import sys as _sys
from collections.abc import Callable as _Callable

from .helpers import *  # make all helpers available at the root level
from .logging import LOGGER
from .logging import setup_logging as _setup_logging

parser = _argparse.ArgumentParser(
    prog="machine-setup",
    description="Setup the machine.",
    epilog="REPO: github.com/mohdfareed/machine",
    formatter_class=_argparse.ArgumentDefaultsHelpFormatter,
)
"""The command line argument parser."""


def startup(
    setup: str | None = None,
    description: str | None = None,
) -> _argparse.Namespace:
    """Parse command line arguments and setup logging."""

    if setup:
        parser.set_defaults(setup=setup)
    if description:
        parser.description = description

    parser.add_argument(
        "-d", "--debug", action="store_true", help="print debug messages"
    )
    args = parser.parse_args()
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
    except SetupError as exception:
        LOGGER.exception(exception)
        LOGGER.error("Setup failed.")
        _sys.exit(1)
    except Exception as exception:  # pylint: disable=broad-except
        LOGGER.exception(exception)
        LOGGER.error("An unexpected error occurred.")
        _sys.exit(1)
    LOGGER.warning("Restart for some changes to apply.")


class SetupError(Exception):
    """Exception due to a setup error."""
