"""Library of modules containing setup methods used for setting up a new
machine. These methods are imported and used by the main `setup.py` script. The
modules in this library depend on modules in the `utils` library."""

from . import brew, git, macos, python, raspberrypi, shell, ssh


def run(setup, printer, message, *args, **kwargs):
    import utils

    try:
        utils.Printer.initialize(debug=True)
        setup(*args, **kwargs)
    except Exception as exception:
        printer.logger.exception(exception)
        printer.error(message)
        exit(1)
