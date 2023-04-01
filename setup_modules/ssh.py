"""Setup module containing a `setup` function for setting up Git on a new
machine.
"""

from resources import ssh_config, ssh_private, ssh_public
from utils import abs_path, copy, shell
from utils.display import Display

DISPLAY: Display = Display(no_logging=True)
"""The default display for printing messages."""

_private_key: str = abs_path("~/.ssh/id_ed25519")
"""The path to the private ssh key."""
_public_key: str = abs_path("~/.ssh/id_ed25519.pub")
"""The path to the public ssh key."""
_config: str = abs_path("~/.ssh/config")
"""The path to the ssh configuration file."""


def setup(display=DISPLAY, quiet=False) -> None:
    """Setup git on a new machine by installing it through Homebrew and
    configuring it.

    A `Display` object is used to print messages and log them to a file. A
    non-logging `Display` object is used by default.

    Args:
        display (Display, optional): The display for printing messages.
    """
    if not quiet:
        display.print("Setting up SSH...")
    else:
        display.debug("")
        display.debug("Setting up SSH...")

    # copy ssh keys and config
    copy(ssh_private, _private_key)
    display.debug(f"Copied: {ssh_private}")
    display.debug(f"    to: {_private_key}")
    copy(ssh_public, _public_key)
    display.debug(f"Copied: {ssh_public}")
    display.debug(f"    to: {_public_key}")
    copy(ssh_config, _config)
    display.debug(f"Copied: {ssh_config}")
    display.debug(f"    to: {_config}")

    # get key fingerprint
    fingerprint = shell.read(f"ssh-keygen -lf '{_public_key}'")
    fingerprint = fingerprint.split(" ")[1]
    display.debug(f"SSH key fingerprint: {fingerprint}")
    # add key to ssh agent if it doesn't exist
    cmd = f"ssh-add -l | grep -q {fingerprint}"
    if shell.run_quiet(cmd, display.verbose) != 0:
        shell.run(f"ssh-add '{_private_key}'", display.print, display.error)
        display.debug("Added ssh key to ssh agent.")

    display.success("SSH was setup successfully.")


if __name__ == "__main__":
    setup()
