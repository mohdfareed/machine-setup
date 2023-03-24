"""Setup module containing a `setup` function for setting up Git on a new
machine.
"""

from utils.display import Display
from utils.shell import Shell


def setup(display: Display = Display(no_logging=True)):
    """Setup macOS on a new machine by installing applications and configuring
    the system.

    A `Display` object is used to print messages and log them to a file. A
    non-logging `Display` object is used by default.

    Args:
        display (Display, optional): The display for printing messages.
    """
    shell = Shell()
    display.header("macOS setup script.")
