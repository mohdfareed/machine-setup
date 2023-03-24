"""Setup module containing a `setup` function for setting up Zsh on a new
machine.
"""

from utils.display import Display
from utils.shell import Shell


def setup(display: Display = Display(no_logging=True)):
    """Setup Zsh on a new machine by symlinking its configuration files.

    A `Display` object is used to print messages and log them to a file. A
    non-logging `Display` object is used by default.

    Args:
        display (Display, optional): The display for printing messages.
    """
    shell = Shell()
    display.header("zsh setup script.")
