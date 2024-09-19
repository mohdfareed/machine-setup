"""Helper functions for setting up the development environment."""

__all__ = [
    "PARSER",
    "SetupError",
    "execute",
    "startup",
]

import argparse
import sys
from collections.abc import Callable
from typing import Any, Optional

from .logging import LOGGER, setup_logging
from .shell import ShellError

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


def execute(setup: Callable[..., None], *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
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
