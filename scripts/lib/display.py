"""Display module that provides functions for printing messages to the
console and logging them to a timestamped file with a severity.
The log file is created in the current working directory and is named
`setup.log`. The log file is overwritten each time the script is run.
The module has a debug mode that can be enabled by calling `debug(True)`. It
causes log messages to be printed to the console in addition to the log file.
"""

from .colors import (bright_red, bright_green, bright_blue, bright_yellow,
                     magenta, bold)
import os
import time


debug = False
"""Whether debug mode is enabled. If set to `True`, log messages are printed
    in magenta to the console. Defaults to `False`."""


def header(message):
    """Prints a bold message to the console proceeded by newlines. The message
    is also logged with the severity of `Header` to the log file, including the
    newline.

    Args:
        message (str): The message to print and log.
    """
    message = f"{message}\n"
    print(bold(message))
    _log(message, "Header")


def error(message):
    """Prints a message in red to the console. The message is also logged with
    the severity of `Error` to the log file.

    Args:
        message (str): The message to print and log.
    """
    print(bright_red(message))
    _log(message, "Error")


def warning(message):
    """Prints a message in yellow to the console. The message is also logged
    with the severity of `Warning` to the log file.

    Args:
        message (str): The message to print and log.
    """
    print(bright_yellow(message))
    _log(message, "Warning")


def info(message):
    """Prints a message in blue to the console. The message is also logged with
    the severity of `Info` to the log file.

    Args:
        message (str): The message to print and log.
    """
    print(bright_blue(message))
    _log(message, "Info")


def success(message):
    """Prints a message in green to the console. The message is also logged with
    the severity of `Success` to the log file.

    Args:
        message (str): The message to print and log.
    """
    print(bright_green(message))
    _log(message, "Success")


def output(message):
    """Prints a message to the console. The message is also logged with the
    severity of `Output` to the log file.

    Args:
        message (str): The message to print and log.
    """
    print(message)
    _log(message, "Output")


def log(message):
    """Log a message to the log file with the severity of `Log`. If debug mode
    is set, the message is also printed in magenta to the console.

    Args:
        message (str): The message to print and log.
    """
    _log(message, "Log")
    if debug:
        print(magenta(message))


def _log(message, level="Debug"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    message = f"[{timestamp}] {level}: {message}\n"
    _log_file.write(message)


def _get_log_file(log_file):
    new_log_file = log_file
    i = 1
    while os.path.exists(new_log_file):
        new_log_file = f"{log_file[:-4]}_{i}.log"
        i += 1
    return new_log_file


def __getattr__(name):
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __exit__():
    _log_file.close()


# set up log file
_log_file = _get_log_file(os.getcwd() + "/setup.log")
_creation_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
_log_file = open(_log_file, 'w+')
_log_file.write('Log created at ' + _creation_time + '\n\n')
