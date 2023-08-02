import logging
import os
from datetime import datetime

from rich import print
from rich.logging import RichHandler

debug_mode = False
"""Whether debug mode is enabled."""


class Printer:
    """A class to print messages to the console and log them to a file."""

    # message format
    _format = r"[bright_black]\[{name}\][/] {message}"

    def __init__(self, name: str):
        self.name = name
        """The name of the printer."""
        self.logger = logging.getLogger(name)
        """The logger for the printer."""

    def title(self, message: str):
        formatted_message = f"\n[bold]{message}[/]"
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
        formatted_message = f"[bold magenta]{message}[/]"
        self.print(message, formatted_message)

    def print(self, message: str, formatted_message: str | None = None):
        formatted_message = formatted_message or message
        self.logger.info(message)
        print(self._format.format(name=self.name, message=formatted_message))

    @staticmethod
    def initialize(to_file=False, debug=False):
        """Initialize the global logger of the printer."""
        global debug_mode
        debug_mode = debug
        logger = logging.getLogger()

        # create console handler
        console_handler = RichHandler(
            markup=True,
            log_time_format="[%Y-%m-%d %H:%M:%S]",
            rich_tracebacks=True,
            tracebacks_show_locals=True,
        )
        format = r"%(message)s [bright_black]- [italic]%(name)s[/italic]"
        console_handler.setFormatter(logging.Formatter(format))
        console_handler.setLevel(logging.WARNING)
        logger.addHandler(console_handler)

        # done if not logging to file
        if not to_file:
            return

        # create file handler
        logging_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(logging_dir, exist_ok=True)
        filename = f"{datetime.now():%y%m%d_%H%M%S}.log"
        file = os.path.join(logging_dir, filename)
        file_handler = logging.FileHandler(file)
        format = "[%(asctime)s] [%(levelname)-8s] %(message)s - %(name)s"
        file_handler.setFormatter(
            logging.Formatter(format, "%Y-%m-%d %H:%M:%S")
        )
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        logger.info(f"Logging to file: {file}")
