"""Setup module containing a `setup` function for setting up Python on a new
machine.
"""

from utils.display import Display
from utils.shell import Shell

_shell = Shell()


def setup(display: Display = Display(no_logging=True)):
    """Setup Python on a new machine by installing it through Homebrew and
    installing its packages.

    A `Display` object is used to print messages and log them to a file. A
    non-logging `Display` object is used by default.

    Args:
        display (Display, optional): The display for printing messages.
    """
    display.header("Python setup script.")
