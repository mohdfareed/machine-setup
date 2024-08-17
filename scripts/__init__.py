"""Library of modules containing setup methods used for setting up a new
machine. These methods are imported and used by the main `setup.py` script. The
modules in this library depend on modules in the `utils` library."""

import logging as _logging
import sys as _sys

import utils as _utils

LOGGER = _logging.getLogger(__name__)
"""The setup logger."""


def run_setup_isolated(setup, *args, **kwargs) -> None:
    """Run a setup method with logging and error handling.
    This function is used to run individual setup methods."""

    run_setup(_utils.setup_logging, debug=True)
    run_setup(setup, *args, **kwargs)


def run_setup(setup, *args, **kwargs) -> None:
    """Run a setup method with logging and error handling."""
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


class SetupError(Exception):
    """A custom exception for setup errors."""
