"""Shell module that provides functions for executing shell commands. The
outputs of the commands are displayed using the `display` module.
"""

import subprocess
import display


shell: str = "/bin/zsh"
"""The shell to use for commands execution."""


def header(message: str):
    """Prints a bold message to the console proceeded by newlines. The message
    is also logged with the severity of `HEADER` to the log file, including the
    newline.

    Args:
        message (str): The message to print and log.
    """
    message = f"{message}\n"
    print((message))
    _log(message, "HEADER")


def _log(message: str, severity: str):
    """Log a message to the log file with a timestamp and the given severity.

    Args:
        message (str): The message to log.
        severity (str): The severity level of the message.
    """
    pass


def __getattr__(name):
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


if __name__ == "__main__":
    # TODO: create a loop that accepts commands, executes them, and displays
    #       the output.
    print("This module is not meant to be run directly.")
    exit(1)
