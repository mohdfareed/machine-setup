"""Module that provides a Display class for printing messages to the console
and logging them to a timestamped file with a severity.
"""

import builtins

from .colors import *
from .logger import Logger


class Display:
    """Display class that provides functions for printing messages to the
    console and logging them to a timestamped file with a severity.

    The module has a verbose mode that can be enabled by setting `verbose_mode`
    to `True`. It causes log messages to be printed to the console in addition
    to the log file. Verbose mode defaults to `False`.
    The module has a debug mode that can be enabled by setting `debug_mode`
    to`True`. It causes debug messages to be printed to the console in addition
    to the log file. Debug mode default to `False`.

    The module has the following log severities:
    - `HEADER`: Indicates the start of a new section.
    - `ERROR`: Indicates a problem or failure.
    - `WARNING`: Indicates a potential problem.
    - `INFO`: Provides additional information.
    - `SUCCESS`: Indicates a successful operation.
    - `OUTPUT`: Both printed to console and logged.
    - `VERBOSE`: Logged but not printed to console unless verbosity is enabled.
    - `DEBUG`: Logged but not printed to console unless debugging is enabled.
    """

    def __init__(self,
                 verbose_mode: bool = False,
                 debug_mode: bool = False,
                 no_logging: bool = False) -> None:
        """Create a new Display object with the provided verbosity, debugging
        and logging settings.

        Args:
            verbose_mode (bool): Turn on verbose mode. Defaults to `False`.
            debug_mode (bool): Turn on debug mode. Defaults to `False`.
            no_logging (bool): Disable logging. Defaults to `False`.
        """
        self.verbose_mode = verbose_mode
        """Whether verbose mode is enabled. If set to `True`, log messages are printed
        in black to the console. Defaults to `False`.
        """
        self.debug_mode = debug_mode
        """Whether debug mode is enabled. If set to `True`, log messages are printed in
        magenta to the console. Defaults to `False`.
        """
        self._logger = Logger(dummy=no_logging)
        """The logger object that manages the main log file of the module.
        """

    def header(self, message: str, logger=None) -> None:
        """Prints a bold message to the console proceeded by a newline. The message
        is also logged with the severity of `HEADER` to the log file, including the
        newline.

        Args:
            message (str): The message to display.
            logger (Logger): The logger to use. Defaults to the main logger.
        """
        logger = logger or self._logger
        builtins.print("\n" + bold(message))
        logger.log(message, "HEADER")

    def error(self, message: str, logger=None) -> None:
        """Prints a message in red to the console. The message is also logged with
        the severity of `ERROR` to the log file.

        Args:
            message (str): The message to display.
            logger (Logger): The logger to use. Defaults to the main logger.
        """
        logger = logger or self._logger
        builtins.print(bright_red(message))
        logger.log(message, "ERROR")

    def warning(self, message: str, logger=None) -> None:
        """Prints a message in yellow to the console. The message is also logged
        with the severity of `WARNING` to the log file.

        Args:
            message (str): The message to display.
            logger (Logger): The logger to use. Defaults to the main logger.
        """
        logger = logger or self._logger
        builtins.print(bright_yellow(message))
        logger.log(message, "WARNING")

    def info(self, message: str, logger=None) -> None:
        """Prints a message in blue to the console. The message is also logged with
        the severity of `INFO` to the log file.

        Args:
            message (str): The message to display.
            logger (Logger): The logger to use. Defaults to the main logger.
        """
        logger = logger or self._logger
        builtins.print(bright_blue(message))
        logger.log(message, "INFO")

    def success(self, message: str, logger=None) -> None:
        """Prints a message in green to the console. The message is also logged with
        the severity of `SUCCESS` to the log file.

        Args:
            message (str): The message to display.
            logger (Logger): The logger to use. Defaults to the main logger.
        """
        logger = logger or self._logger
        builtins.print(bright_green(message))
        logger.log(message, "SUCCESS")

    def print(self, message: str, logger=None) -> None:
        """Prints a message to the console. The message is also logged with the
        severity of `LOG` to the log file.

        Args:
            message (str): The message to display.
            logger (Logger): The logger to use. Defaults to the main logger.
        """
        logger = logger or self._logger
        builtins.print(message)
        logger.log(message, "LOG")

    def verbose(self, message: str, logger=None) -> None:
        """Log a message to the log file with the severity of `VERBOSE`. If verbose
        mode is set, the message is also printed in black to the console.

        Args:
            message (str): The message to display.
            logger (Logger): The logger to use. Defaults to the main logger.
        """
        logger = logger or self._logger
        if self.verbose_mode:
            builtins.print(black(message))
        logger.log(message, "VERBOSE")

    def debug(self, message: str, logger=None) -> None:
        """Log a message to the log file with the severity of `DEBUG`. If debug
        mode is set, the message is also printed in magenta to the console.

        Args:
            message (str): The message to display.
            logger (Logger): The logger to use. Defaults to the main logger.
        """
        logger = logger or self._logger
        if self.debug_mode:
            builtins.print(magenta(message))
        logger.log(message, "DEBUG")

    def __call__(self) -> None:
        """Prints a newline to the console without logging it to the log file.
        """
        print("")


def __getattr__(name):
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


if __name__ == "__main__":
    builtins.print("This module is not meant to be run directly.")
    exit(1)
