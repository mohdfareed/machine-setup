"""SSH setup module."""

import os
from collections import defaultdict
from typing import Optional

import config
import utils

SSH_DIR: str = "~/.ssh/"
"""The path to the SSH directory."""
PRIVATE_KEY_EXTENSION: str = ".key"
"""The extension of the private key files."""
PUBLIC_KEY_EXTENSION: str = ".pub"
"""The extension of the public key files."""

printer = utils.Printer("ssh")
"""The SSH setup printer."""
shell = utils.Shell(printer.debug, printer.error)
"""The SSH shell instance."""


class SSHKey:
    def __init__(self) -> None:
        self.private_key: Optional[str] = None
        """The path to the private key file."""
        self.public_key: Optional[str] = None
        """The path to the public key file."""


def setup(keys_dir: Optional[str]) -> None:
    """Setup ssh keys and configuration on a new machine. The ssh keys and
    config file are copied from the specified directory.

    Args:
        keys_dir (str): The path to the directory containing the ssh keys.
    """
    printer.info("Setting up SSH...")

    # copy config file
    utils.symlink(config.ssh_config, SSH_DIR + "config")
    if not keys_dir:
        return

    # setup ssh keys
    key_pairs = load_keys(keys_dir)
    for key_name, key in key_pairs.items():
        setup_key(key_name, key)
    printer.success("SSH setup complete")


def load_keys(keys: str) -> dict[str, SSHKey]:
    """Load ssh keys from the specified directory.

    Returns:
        dict[str, SSHKey]: A dict of key names to key pairs.
    """
    keys = utils.abspath(keys)

    # load keys as dictionary of key names to key pairs
    keys_dict: dict[str, SSHKey] = defaultdict(SSHKey)
    for filename in os.listdir(keys):
        key_name = os.path.splitext(filename)[0]

        # add key to dictionary
        filepath = os.path.realpath(os.path.join(keys, filename))
        if filename.endswith(PRIVATE_KEY_EXTENSION):
            keys_dict[key_name].private_key = filepath
        elif filename.endswith(PUBLIC_KEY_EXTENSION):
            keys_dict[key_name].public_key = filepath

    loaded_keys = ", ".join(keys_dict.keys())
    printer.debug(f"Loaded [bold]{len(keys_dict)}[/] ssh keys: " + loaded_keys)
    return keys_dict


def setup_key(name: str, key: SSHKey) -> None:
    printer.print(f"[bold]Setting up SSH key:[/] {name}")
    if not key.private_key or not key.public_key:
        printer.error(f"Invalid ssh key pair:")
        printer.error(f"    Private key: {key.private_key}")
        printer.error(f"    Public key: {key.public_key}")
        raise RuntimeError(f"Invalid ssh key pair encountered: {name}")

    # symlink key and set permissions
    utils.symlink(key.private_key, SSH_DIR)
    utils.chmod(key.private_key, 600)
    utils.symlink(key.public_key, SSH_DIR)
    utils.chmod(key.public_key, 644)

    # get key fingerprint
    fingerprint = shell(["ssh-keygen", "-lf", key.public_key], silent=True)[0]
    fingerprint = fingerprint.split(" ")[1]
    printer.print(f"[bold]Key fingerprint:[/] {fingerprint}")

    # add key to ssh agent if it doesn't exist
    cmd = "ssh-add -l | grep -q " + fingerprint
    if shell(cmd, silent=True)[1] != 0:
        shell(f"ssh-add '{key.private_key}'")
        printer.print("Added key to SSH agent")
    else:
        printer.print("Key already exists in SSH agent")
    printer.success("Key setup complete")


if __name__ == "__main__":
    import argparse

    import core

    parser = argparse.ArgumentParser(description="SSH setup script.")
    parser.add_argument(
        "keys", type=str, help="the path to the ssh keys directory"
    )
    args = parser.parse_args()
    core.run(setup, printer, "Failed to setup SSH", args.keys)
