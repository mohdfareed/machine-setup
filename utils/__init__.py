"""Utilities library containing modules and functions used within the project.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler

LOGGER = logging.getLogger()
"""The root logger."""

machine_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
"""The root directory of the machine."""
logging_file = os.path.join(machine_root, "logs", "setup.log")
"""The path to the logging file."""
reduced_logging_modules = []  # modules with reduced (WARNING) logging level


def setup_logging(debug: bool = False) -> None:
    """Setup the logging configuration.

    Args:
        debug (bool): Whether to enable debug mode.
    """
    # logging formats
    console_formatter = logging.Formatter(
        r"%(message)s [bright_black]- [italic]%(name)s[/italic] "
        r"\[[underline]%(filename)s:%(lineno)d[/underline]]",
        datefmt=r"%Y-%m-%d %H:%M:%S.%f",
    )
    file_formatter = logging.Formatter(
        r"[%(asctime)s.%(msecs)03d] %(levelname)-8s "
        r"%(message)s - %(name)s [%(filename)s:%(lineno)d]",
        datefmt=r"%Y-%m-%d %H:%M:%S",
    )

    # setup console logger
    console_handler = RichHandler(
        markup=True,
        show_path=False,
        tracebacks_show_locals=debug,
        rich_tracebacks=True,
        tracebacks_width=80,
    )
    console_handler.setFormatter(console_formatter)

    # setup file logger
    os.makedirs(os.path.dirname(logging_file), exist_ok=True)
    file_handler = RotatingFileHandler(
        logging_file, maxBytes=2**20, backupCount=10
    )
    file_handler.setFormatter(file_formatter)

    # configure logging
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if debug else logging.INFO)
    root_logger.handlers = [console_handler, file_handler]
    logging.captureWarnings(True)

    # reduce logging level for some modules
    for module in reduced_logging_modules:
        logging.getLogger(module).setLevel(logging.WARNING)
