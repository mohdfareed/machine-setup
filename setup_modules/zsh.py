"""Setup module containing a `setup` function for setting up the shell on a new
machine.
"""

from resources import zshrc
from utils import abs_path, create_file, shell, symlink
from utils.display import Display

from .homebrew import install_package

DISPLAY: Display = Display(no_logging=True)
"""The default display for printing messages."""

_zshrc: str = abs_path("~/.zshrc")
"""The path to the zsh configuration file symlink."""


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

    # install zsh and plugins
    install_package(display, "zsh")
    install_package(display, "zsh-completions")
    install_package(display, "zsh-autosuggestions")
    install_package(display, "zsh-syntax-highlighting")
    install_package(display, "spaceship")
    display.debug("Packages were installed.")

    # symlink configuration file
    symlink(zshrc, _zshrc)
    display.debug(f"Symlinked: {zshrc}")
    display.debug(f"       to: {_zshrc}")
    # remove last login time prompt
    create_file("~/.hushlogin")
    display.debug("Removed last login time prompt.")

    display.success("Shell was setup successfully.")


if __name__ == "__main__":
    setup()
