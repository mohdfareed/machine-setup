from utils import Display


def setup(display: Display = Display(no_logging=True)):
    """Setup macOS on a new machine by installing applications and configuring
    the system.

    A `Display` object is used to print messages and log them to a file. A
    non-logging `Display` object is used by default.

    Args:
        display (Display, optional): The display for printing messages.
    """
    display.header("macOS setup script.")
