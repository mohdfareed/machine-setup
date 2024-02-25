"""Library of modules containing setup methods used for setting up a new
machine. These methods are imported and used by the main `setup.py` script. The
modules in this library depend on modules in the `utils` library."""


def run(setup, logger, message, *args, **kwargs):
    import utils

    try:
        utils.setup_logging(debug=True)
        setup(*args, **kwargs)
    except Exception as exception:
        logger.exception(exception)
        logger.error(message)
        exit(1)
