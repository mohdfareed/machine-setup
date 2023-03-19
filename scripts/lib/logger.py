"""Module that contains the Logger class, which manages log file. The log file
is created at the current working directory with the filename
`setup_{current_date}_{current_time}.log`. It provides a `log` methods to log
messages to the file with a timestamp and severity.
"""

import os
from datetime import datetime


class Logger:
    """Class that manages the log file. The file is created when the class is
    instantiated and closed when the class is destroyed.
    """

    from typing import TextIO
    log_file: TextIO
    """File to which messages are logged. The file is created on module import
    at working directory with the filename
    `setup_{current_date}_{current_time}.log`. It is opened in write mode and
    closed when the module is exited.
    """

    def __init__(self):
        """Create a new log file at the current working directory with the
        filename `setup_{current_date}_{current_time}.log`. If a file with that
        name already exists, a counter is appended to the filename.
        """
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{os.getcwd()}/setup_{current_datetime}.log"
        counter = 'a'
        while os.path.exists(filename):
            filename = filename.replace(".log", f"_{counter}.log")
            counter = chr(ord(counter) + 1)
        self.log_file = open(filename, 'w+')

    def log(self, message: str, severity: str):
        """Log a message to the log file with a timestamp and the specified
        severity in the format: `[timestamp] severity: {message}`.

        Args:
            message (str): The message to log.
            severity (str): The severity level of the message.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {severity}: {message}\n"
        self.log_file.write(log_entry)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.log_file.close()


def __getattr__(name):
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


if __name__ == "__main__":
    print("This module is not meant to be run directly.")
    exit(1)
