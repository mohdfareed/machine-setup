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

    def __init__(self, dummy: bool = False) -> None:
        """Create a new log file at the current working directory with the
        filename `setup_{current_date}_{current_time}.log`. If a file with that
        name already exists, a counter is appended to the filename.

        A dummy logger can be created that does not create a log file. This
        prevents the log method from taking any action. Defaults to `False`.

        Args:
            dummy (bool): Set to `True` to not create a log file.
        """
        self.is_dummy = dummy
        """Whether the logger is a dummy logger. If set to `True`, the log
        method is a no-op. Defaults to `False`.
        """
        if self.is_dummy:
            return

        current_datetime = datetime.now().strftime("%y%m%d_%H%M%S")
        filename = f"{os.getcwd()}/setup_{current_datetime}.log"
        counter = 1
        while os.path.exists(filename):
            filename = filename.replace(".log", f"_{counter}.log")
            counter += 1

        self.log_file = open(filename, "w+")
        """File to which messages are logged. The file is created on module
        import at working directory with the filename
        `setup_{current_date}_{current_time}.log`. It is opened in write mode
        and closed when the module is exited.
        """

    def log(self, message: str, severity: str) -> None:
        """Log a message to the log file with a timestamp and the specified
        severity in the format: `[timestamp] severity: {message}`.

        Args:
            message (str): The message to log.
            severity (str): The severity level of the message.
        """
        if self.is_dummy or not self.log_file:
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {severity}: {message.strip()}\n"
        self.log_file.write(log_entry)
        self.log_file.flush()


def __getattr__(name):
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


if __name__ == "__main__":
    print("This module is not meant to be run directly.")
    exit(1)
