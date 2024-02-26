"""Library of modules containing setup methods used for setting up a new
machine. These methods are imported and used by the main `setup.py` script. The
modules in this library depend on modules in the `utils` library."""

import logging

LOGGER = logging.getLogger(__name__)
"""The setup logger."""


def run_setup_isolated(setup, *args, **kwargs):
    """Run a setup method with logging and error handling.
    This function is used to run individual setup methods."""
    import utils

    run_setup(utils.setup_logging, debug=True)
    run_setup(utils.setup_sudo)
    run_setup(setup, *args, **kwargs)


def run_setup(setup, *args, **kwargs):
    """Run a setup method with logging and error handling."""
    try:
        setup(*args, **kwargs)
    except KeyboardInterrupt:
        print()
        LOGGER.warning("Setup interrupted.")
        exit(0)
    except Exception as exception:
        LOGGER.exception(exception)
        LOGGER.error(f"Setup failed.")
        exit(1)
