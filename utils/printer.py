import logging
import os
from datetime import datetime

from rich import print
from rich.logging import RichHandler

import utils

debug_mode = False
"""Whether debug mode is enabled."""
printer: "Printer"
"""The main printer."""


class Printer:
    """A class to print messages to the console and log them to a file."""

    # messages format
    _format = r"[bright_black]\[{name}][/] {message}"

    def __init__(self, name: str):
        self.name = name
        """The name of the printer."""
        self.logger = logging.getLogger(self.name)
        """The logger of the printer."""

    def title(self, message: str):
        print()
        formatted_message = f"[bold]{message}[/]"
        self.print(message, formatted_message)

    def success(self, message: str):
        formatted_message = f"[bold green]{message}[/]"
        self.print(message, formatted_message)

    def error(self, message: str):
        formatted_message = f"[bold red]{message}[/]"
        self.print(message, formatted_message)

    def warning(self, message: str):
        formatted_message = f"[bold yellow]{message}[/]"
        self.print(message, formatted_message)

    def info(self, message: str):
        formatted_message = f"[bold blue]{message}[/]"
        self.print(message, formatted_message)

    def debug(self, message: str):
        formatted_message = f"[magenta]{message}[/]"
        if not debug_mode:
            self.logger.info(message)
            return
        self.print(message, formatted_message)

    def print(self, message: str, formatted_message: str | None = None):
        formatted_message = formatted_message or message
        print(self._format.format(name=self.name, message=formatted_message))

        # self.logger = self.logger or logging.getLogger(self.name)
        self.logger.info(message)

    @staticmethod
    def initialize(to_file=False, debug=False):
        """Initialize the global logger of the printer."""
        global debug_mode, printer
        debug_mode = debug
        printer = Printer("root")
        printer.debug(f"Debug mode enabled") if debug else None

        # setup root logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logging.captureWarnings(True)

        # create console handler
        console_handler = _create_console_handler()
        logger.addHandler(console_handler)

        if to_file:  # create file handler
            file_handler, file = _create_file_handler()
            printer.info(f"Logging to file: {file}")
            logger.addHandler(file_handler)


def _create_console_handler():
    console_handler = RichHandler(
        markup=True,
        log_time_format="[%Y-%m-%d %H:%M:%S]",
        rich_tracebacks=True,
        tracebacks_show_locals=True,
    )
    format = r"%(message)s [bright_black]- [italic]%(name)s[/italic]"
    console_handler.setFormatter(logging.Formatter(format))
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
