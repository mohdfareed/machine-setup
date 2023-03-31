"""Setup module containing a `setup` function for setting up the shell on a new
machine.
"""

from resources import zshrc
from utils.display import Display
from utils import symlink, HOME, shell
from .homebrew import install_package

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

    # check if homebrew is installed
    if shell.run('command -v brew', display.verbose, display.error) != 0:
        raise RuntimeError("Could not find Homebrew.")
    display.debug("Homebrew was found.")

    # install zsh and pure prompt
    install_package(display, "zsh", 'brew', "Zsh")
    install_package(display, "pure", 'brew', "Pure prompt")
    display.debug("Packages were installed.")

    # symlink configuration file
    symlink(zshrc, "~/.zshrc")
    display.debug("Created symbolic links.")
    # remove last login time prompt
    open(f"{HOME}/.hushlogin", "a").close()
    display.debug("Removed last login time prompt.")

    display.success("Shell was setup successfully.")


if __name__ == "__main__":
    setup()
