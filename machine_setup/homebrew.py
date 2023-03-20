"""Setup module containing a `setup` function for setting up Homebrew on a new
machine.
"""

from utils import Display
from utils import shell


def setup(display: Display = Display(no_logging=True)):
    """Setup Homebrew on a new machine by installing Homebrew and its packages.
    A `Display` object is used to print messages and log them to a file. A
    non-logging `Display` object is used by default.

    Args:
        display (Display, optional): The display for printing messages.
    """
    display.header("Setting up Homebrew...")
    display.print("Installing Homebrew...")

    shell.run("echo hello world", display.print, display.error)
    shell.run_quiet("echo hello world", shell.loader, display.verbose)


if __name__ == "__main__":
    setup()
