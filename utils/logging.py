"""Logging configuration for the project."""

__all__ = ["LOGGER", "setup_logging"]

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler

LOGGER = logging.getLogger(__name__)
"""The utils logger."""

machine_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
logging_dir = os.path.join(machine_root, "logs")
reduced_logging_modules: list[str] = []  # modules with reduced (WARNING) logging level


def setup_logging(debug: bool = False) -> None:
    """Setup the logging configuration.

    Args:
        debug (bool): Whether to enable debug mode.
    """
    # logging formats
    console_formatter = logging.Formatter(r"%(message)s")
    file_formatter = logging.Formatter(
        r"[%(asctime)s.%(msecs)03d] %(levelname)-8s "
        r"%(message)s - %(name)s [%(filename)s:%(lineno)d]",
        datefmt=r"%Y-%m-%d %H:%M:%S",
    )

    # setup console logger
    console_handler = RichHandler(
        show_time=False,
        show_path=True,
        tracebacks_show_locals=debug,
        rich_tracebacks=True,
    )
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)

    # create a new log file with a descriptive name
    os.makedirs(logging_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logging_filename = f"{timestamp}.log"
    logging_file = os.path.join(logging_dir, logging_filename)

    # setup file logger
    os.makedirs(os.path.dirname(logging_file), exist_ok=True)
    file_handler = RotatingFileHandler(logging_file, maxBytes=2**20, backupCount=10)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)  # log all messages to file

    # configure logging
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers = [console_handler, file_handler]
    logging.captureWarnings(True)
    # reduce logging level for some modules
    for module in reduced_logging_modules:
        logging.getLogger(module).setLevel(logging.WARNING)
