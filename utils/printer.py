import logging
import os
from datetime import datetime
from typing import Optional

from rich import print
from rich.logging import RichHandler

import utils


class Printer:
    """A class to print messages to the console and log them to a file."""

    debug_mode = True
    """Whether debug mode is enabled."""
    # messages format
    _format = r"[bright_black]\[{name}][/] {message}"

    def __init__(self, name: str):
        self.name = name
        """The name of the printer."""
        self.logger = logging.getLogger(self.name)
        """The logger of the printer."""

    def success(self, message: str, *args, **kwargs):
        formatted_message = f"[bold green]{message}[/]"
        self.print(message, formatted_message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        formatted_message = f"[bold red]{message}[/]"
        self.print(message, formatted_message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        formatted_message = f"[bold yellow]{message}[/]"
        self.print(message, formatted_message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        formatted_message = f"[bold blue]{message}[/]"
        self.print(message, formatted_message, *args, **kwargs)

    def debug(self, message: str, *args, **kwargs):
        formatted_message = f"[magenta]{message}[/]"
        if not self.debug_mode:
            self.logger.info(message)
            return
        self.print(message, formatted_message, *args, **kwargs)

    def print(self, msg: str, styled: Optional[str] = None, *args, **kwargs):
        styled = styled or msg
        formatted_msg = self._format.format(name=self.name, message=styled)
        print(formatted_msg, *args, **kwargs)
        self.logger.info(msg) if msg else None

    @classmethod
    def initialize(cls, to_file=False, debug=False):
        """Initialize the global logger of the printer."""
        if to_file:  # create file handler
            file_handler, file = _create_file_handler()
            utils.root_printer.info(f"Logging to file: {file}")
            logger.addHandler(file_handler)
        cls.debug_mode = debug
        utils.root_printer.debug("Debug mode enabled") if debug else None


def _create_console_handler():
    console_handler = RichHandler(
        markup=True,
        log_time_format="[%Y-%m-%d %H:%M:%S]",
        rich_tracebacks=True,
        tracebacks_show_locals=True,
    )
    console_handler.setFormatter(logging.Formatter(r"%(message)s"))
    console_handler.setLevel(logging.WARNING)
    return console_handler


def _create_file_handler():
    # create logging file
    filename = f"{datetime.now():%y%m%d_%H%M%S}.log"
    logging_dir = utils.abspath(os.getcwd(), "logs")
    utils.create_dir(logging_dir)
    file = utils.abspath(logging_dir, filename)
    # create file handler
    file_handler = logging.FileHandler(file)
    format = "[%(asctime)s] [%(levelname)-8s] %(message)s - %(name)s"
    file_handler.setFormatter(logging.Formatter(format, "%Y-%m-%d %H:%M:%S"))
    file_handler.setLevel(logging.DEBUG)
    return file_handler, file


# setup root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.captureWarnings(True)

# create console handler
console_handler = _create_console_handler()
logger.addHandler(console_handler)
