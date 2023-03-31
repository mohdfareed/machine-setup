"""Setup module containing a `setup` function for setting up the shell on a new
machine.
"""

import os

from resources import zshrc
from utils.display import Display

DISPLAY: Display = Display(no_logging=True)
"""The default display for printing messages."""


def setup(display=DISPLAY) -> None:
    """Setup the shell on a new machine by symlinking its configuration files.

    A `Display` object is used to print messages and log them to a file. A
    non-logging `Display` object is used by default.

    Args:
        display (Display, optional): The display for printing messages.
    """
    display.header("Setting up shell...")
    home = os.path.expanduser("~")

    # symlink configuration file
    zshrc_symlink = os.path.join(home, ".zshrc")
    os.remove(zshrc_symlink) if os.path.exists(zshrc_symlink) else None
    os.symlink(zshrc, zshrc_symlink)

    # remove last login time prompt
    open(os.path.join(home, ".hushlogin"), "a").close()


if __name__ == "__main__":
    setup()
