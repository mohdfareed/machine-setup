"""Setup module containing a `setup` function for setting up Git on a new
machine.
"""

from utils import abs_path, create_file, shell, symlink
from utils.display import Display

from ..git import gitconfig, gitignore

DISPLAY: Display = Display(no_logging=True)
"""The default display for printing messages."""

_gitconfig: str = abs_path("~/.gitconfig")
"""The path to the git configuration file on the machine."""
_gitignore: str = abs_path("~/.gitignore")
"""The path to the git ignore file on the machine."""


def setup(display=DISPLAY) -> None:
    """Setup git on a new machine by installing it through Homebrew and
    configuring it.

    A `Display` object is used to print messages and log them to a file. A
    non-logging `Display` object is used by default.

    Args:
        display (Display, optional): The display for printing messages.
    """
    display.header("Setting up Git...")

    # check if homebrew is installed and install git
    if shell.run("command -v brew", display.debug, display.error) != 0:
        raise RuntimeError("Could not find Homebrew.")
    display.verbose("Homebrew was found.")

    # symlink configuration file
    symlink(gitconfig, _gitconfig)
    display.verbose(f"Symlinked: {gitconfig}")
    display.verbose(f"       to: {_gitconfig}")
    symlink(gitignore, _gitignore)
    display.verbose(f"Symlinked: {gitconfig}")
    display.verbose(f"       to: {_gitignore}")

    # set github as a known host if it doesn't exist
    if shell.run_quiet(f"ssh-keygen -F github.com", display.debug) != 0:
        create_file("~/.ssh/known_hosts")
        cmd = f"ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts"
        if shell.run(cmd, display.debug, display.error) != 0:
            raise RuntimeError("Failed to set github as a known host.")
        display.verbose("Github was set as a known host.")

    display.success("Git was setup successfully.")


if __name__ == "__main__":
    setup()
