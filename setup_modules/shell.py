"""Setup module containing a `setup` function for setting up the shell on a new
machine.
"""

from utils import shell
from utils.display import Display

DISPLAY: Display = Display(no_logging=True)
"""The default display for printing messages."""


def setup(display=DISPLAY) -> None:
    """Setup the shell on a new machine by symlinking its configuration files.

    A `Display` object is used to print messages and log them to a file. A
    non-logging `Display` object is used by default.

    Args:
        display (Display, optional): The display for printing messages.
        shell (Shell, optional): The shell for running commands.
        silent (bool, optional): Whether to run the script silently.
    """
    display.header("Setting up shell...")

    # symlink files
    # ln -sfv "$zsh_dir/zshrc" "$ZDOTDIR/.zshrc"

    # remove last login time prompt
    # touch "$HOME/.hushlogin"


if __name__ == "__main__":
    setup()
