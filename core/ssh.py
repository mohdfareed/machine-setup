"""Setup module containing a `setup` function for setting up Git on a new
machine.
"""

from utils import abs_path, chmod, copy, shell
from utils.display import Display

DISPLAY: Display = Display(no_logging=True)
"""The default display for printing messages."""

_private_key: str = abs_path("~/.ssh/id_ed25519")
"""The path to the private ssh key on the machine."""
_public_key: str = abs_path("~/.ssh/id_ed25519.pub")
"""The path to the public ssh key on the machine."""
_config: str = abs_path("~/.ssh/config")
"""The path to the ssh configuration file on the machine."""


def setup(ssh_dir: str, display=DISPLAY, quiet=False) -> None:
    """Setup ssh keys and configuration on a new machine. The ssh keys and
    config file are copied from the specified directory.

    A `Display` object is used to print messages and log them to a file. A
    non-logging `Display` object is used by default.

    Args:
        ssh_dir (str): The path to the directory containing the ssh files.
        display (Display, optional): The display for printing messages.
    """
    if not quiet:
        display.print("Setting up SSH...")
    else:
        display.debug("")
        display.debug("Setting up SSH...")

    # set ssh paths
    private_key = abs_path(f"{ssh_dir}/id_ed25519")
    public_key = abs_path(f"{ssh_dir}/id_ed25519.pub")
    config = abs_path(f"{ssh_dir}/config")

    # copy private key
    copy(private_key, _private_key)
    display.debug(f"Copied: {private_key}")
    display.debug(f"    to: {_private_key}")
    # copy public key
    copy(public_key, _public_key)
    display.debug(f"Copied: {public_key}")
    display.debug(f"    to: {_public_key}")
    # copy config file
    copy(config, _config)
    display.debug(f"Copied: {config}")
    display.debug(f"    to: {_config}")

    try:  # set permissions of ssh keys
        chmod(_private_key, 600)
        chmod(_public_key, 644)
    except:
        raise RuntimeError("Failed to set permissions of ssh keys.")

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
    import argparse

    # parse command line arguments
    parser = argparse.ArgumentParser(description="SSH setup script.")
    parser.add_argument(
        "--ssh-dir",
        type=str,
        required=True,
        help="the path to the ssh directory of keys",
    )
    args = parser.parse_args()
    # setup ssh using the specified directory
    setup(args.ssh_dir)
