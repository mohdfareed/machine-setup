"""Display module that provides functions for printing messages to the console
and logging them to a timestamped file with a severity.
The log file is created at the current working directory with the filename
`setup_{current_date}_{current_time}.log`.

The module has a verbose mode that can be enabled by setting `verbose_mode` to
`True`. It causes log messages to be printed to the console in addition to the
log file. Verbose mode defaults to `False`.
The module has a debug mode that can be enabled by setting `debug_mode` to
`True`. It causes debug messages to be printed to the console in addition to
the log file. Debug mode default to `False`.

The module has the following log severities:
- `HEADER`: Indicates the start of a new section.
- `ERROR`: Indicates a problem or failure.
- `WARNING`: Indicates a potential problem.
- `INFO`: Provides additional information.
- `SUCCESS`: Indicates a successful operation.
- `OUTPUT`: Both printed to console and logged.
- `VERBOSE`: Logged but not printed to console unless verbose mode is enabled.
- `DEBUG`: Logged but not printed to console unless debug mode is enabled.
"""

import os
import time
from io import TextIOWrapper
from .colors import *


verbose_mode: bool = False
"""Whether verbose mode is enabled. If set to `True`, log messages are printed
    in magenta to the console. Defaults to `False`."""

debug_mode: bool = False
"""Whether debug mode is enabled. If set to `True`, log messages are printed
    in magenta to the console. Defaults to `False`."""

_log_file: TextIOWrapper = None  # type: ignore
"""File to which messages are logged. The file is created on module import at
working directory with the filename `setup_{current_date}_{current_time}.log`.
It is opened in write mode and closed when the module is exited.
"""


def header(message: str):
    """Prints a bold message to the console proceeded by newlines. The message
    is also logged with the severity of `HEADER` to the log file, including the
    newline.

    Args:
        message (str): The message to print and log.
    """
    message = f"{message}\n"
    print(bold(message))
    _log(message, "HEADER")


def error(message: str):
    """Prints a message in red to the console. The message is also logged with
    the severity of `ERROR` to the log file.

    Args:
        message (str): The message to print and log.
    """
    print(bright_red(message))
    _log(message, "ERROR")


def warning(message: str):
    """Prints a message in yellow to the console. The message is also logged
    with the severity of `WARNING` to the log file.

    Args:
        message (str): The message to print and log.
    """
    print(bright_yellow(message))
    _log(message, "WARNING")


def info(message: str):
    """Prints a message in blue to the console. The message is also logged with
    the severity of `INFO` to the log file.

    Args:
        message (str): The message to print and log.
    """
    print(bright_blue(message))
    _log(message, "INFO")


def success(message: str):
    """Prints a message in green to the console. The message is also logged with
    the severity of `SUCCESS` to the log file.

    Args:
        message (str): The message to print and log.
    """
    print(bright_green(message))
    _log(message, "SUCCESS")


def output(message: str):
    """Prints a message to the console. The message is also logged with the
    severity of `OUTPUT` to the log file.

    Args:
        message (str): The message to print and log.
    """
    print(message)
    _log(message, "OUTPUT")


def verbose(message: str):
    """Log a message to the log file with the severity of `VERBOSE`. If verbose
    mode is set, the message is also printed in black to the console.

    Args:
        message (str): The message to print and log.
    """
    _log(message, "VERBOSE")
    if verbose_mode:
        print(message)


def debug(message: str):
    """Log a message to the log file with the severity of `DEBUG`. If debug
    mode is set, the message is also printed in magenta to the console.

    Args:
        message (str): The message to print and log.
    """
    _log(message, "DEBUG")
    if debug_mode:
        print(magenta(message))


def _log(message: str, severity: str):
    """Log a message to the log file with a timestamp and the given severity.

    Args:
        message (str): The message to log.
        severity (str): The severity level of the message.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    message = f"[{timestamp}] {severity}: {message}\n"
    _log_file.write(message)


def __enter__():
    global _log_file
    _current_datetime = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    _log_file = open(f"{os.getcwd()}/setup_{_current_datetime}.log", 'w+')


def __exit__():
    _log_file.close()


def __getattr__(name):
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


if __name__ == "__main__":
    print("This module is not meant to be run directly.")
    exit(1)
