"""Setup module containing a `setup` function for setting up Git on a new
machine.
"""

from config import macos_preferences, terminal_dark, terminal_light
from utils import shell
from utils.display import Display

DISPLAY: Display = Display(verbose=True, no_logging=True)
"""The default display for printing messages."""


def setup(display=DISPLAY) -> None:
    """Setup macOS on a new machine by installing applications and configuring
    the system.

    A `Display` object is used to print messages and log them to a file. A
    non-logging `Display` object is used by default.

    Args:
        display (Display, optional): The display for printing messages.
    """
    display.header("macOS setup script.")

    # add terminal profiles
    cmd = f"open -g '{terminal_dark}'"
    shell.run(cmd, display.debug)
    cmd = f"open -g '{terminal_light}'"
    shell.run(cmd, display.debug)

    # run the macOS preferences script
    if shell.run(f". {macos_preferences}", display.debug) != 0:
        display.info("Check the log file for more information.")
        raise RuntimeError("Setting macOS preferences failed.")

    display.success("macOS was setup successfully.")


if __name__ == "__main__":
    setup()
