"""Setup module containing a `setup` function for setting up Git on a new
machine.
"""

from resources import macos_preferences
from utils import shell
from utils.display import Display

DISPLAY: Display = Display(verbose=True)
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

    # run the macOS preferences script
    if shell.run(f'. {macos_preferences}', display.verbose) != 0:
        display.info("Check the log file for more information.")
        raise RuntimeError("Setting macOS preferences failed.")

    display.success("macOS was setup successfully.")


if __name__ == "__main__":
    setup()
