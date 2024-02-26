"""Library of modules containing setup methods used for setting up a new
machine. These methods are imported and used by the main `setup.py` script. The
modules in this library depend on modules in the `utils` library."""


def run_setup(setup, *args, **kwargs):
    """Run a setup method with logging and error handling.
    This function is used to run individual setup methods."""
    import logging

    import utils

    try:
        utils.setup_logging(debug=True)
        utils.setup_sudo()
        setup(*args, **kwargs)
    except KeyboardInterrupt:
        print()
        logging.getLogger(__name__).warning("Setup interrupted.")
        exit(0)
    except Exception as exception:
        logging.getLogger(__name__).exception(exception)
        logging.getLogger(__name__).error(f"Setup failed.")
        exit(1)
