"""SSH setup module."""

import logging
import os
from collections import defaultdict
from typing import Optional

import config

SSH_DIR: str = "~/.ssh/"
"""The path to the SSH directory."""
PRIVATE_KEY_EXTENSION: str = ".key"
"""The extension of the private key files."""
PUBLIC_KEY_EXTENSION: str = ".pub"
"""The extension of the public key files."""

LOGGER = logging.getLogger(__name__)
"""The SSH setup logger."""


class SSHKey:
    def __init__(self) -> None:
        self.private_key: Optional[str] = None
        """The path to the private key file."""
        self.public_key: Optional[str] = None
        """The path to the public key file."""


def setup() -> None:
    """Setup ssh keys and configuration on a new machine. The ssh keys and
    config file are copied from the specified directory.

    Args:
        keys_dir (str): The path to the directory containing the ssh keys.
    """
    LOGGER.info("Setting up SSH...")

    # copy config file
    os.makedirs(SSH_DIR, exist_ok=True)
    os.remove(config.ssh_config)
    os.symlink(config.ssh_config, os.path.join(SSH_DIR, "config"))

    if keys_dir:  # setup ssh keys
        key_pairs = load_keys(keys_dir)
        [setup_key(key_name, key) for key_name, key in key_pairs.items()]
    LOGGER.info("SSH setup complete")


def load_keys(keys: str) -> dict[str, SSHKey]:
    """Load ssh keys from the specified directory.

    Returns:
        dict[str, SSHKey]: A dict of key names to key pairs.
    """
    keys = os.path.abspath(keys)

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
    LOGGER.debug(f"Loaded [bold]{len(keys_dict)}[/] ssh keys: " + loaded_keys)
    return keys_dict


def setup_key(name: str, key: SSHKey) -> None:
    LOGGER.info(f"[bold]Setting up SSH key:[/] {name}")
    if not key.private_key or not key.public_key:
        LOGGER.error("Invalid ssh key pair:")
        LOGGER.error(f"    Private key: {key.private_key}")
        LOGGER.error(f"    Public key: {key.public_key}")
        raise RuntimeError(f"Invalid ssh key pair encountered: {name}")

    # symlink keys and fix permissions
    os.makedirs(SSH_DIR, exist_ok=True)
    os.remove(key.private_key)
    os.symlink(
        key.private_key, os.path.join(SSH_DIR, name + PRIVATE_KEY_EXTENSION)
    )
    os.chmod(key.private_key, 0o600)
    os.remove(key.public_key)
    os.symlink(
        key.public_key, os.path.join(SSH_DIR, name + PUBLIC_KEY_EXTENSION)
    )
    os.chmod(key.public_key, 0o644)

    # get key fingerprint
    fingerprint = shell(["ssh-keygen", "-lf", key.public_key], silent=True)[0]
    fingerprint = fingerprint.split(" ")[1]
    LOGGER.info(f"[bold]Key fingerprint:[/] {fingerprint}")

    # add key to ssh agent if it doesn't exist
    cmd = "ssh-add -l | grep -q " + fingerprint
    if shell(cmd, silent=True, safe=True)[1] != 0:
        shell(f"ssh-add '{key.private_key}'")
        LOGGER.info("Added key to SSH agent")
    else:
        LOGGER.info("Key already exists in SSH agent")
    LOGGER.info("Key setup complete")


if __name__ == "__main__":
    import argparse

    import scripts

    parser = argparse.ArgumentParser(description="SSH setup script.")
    parser.add_argument(
        "keys", type=str, help="the path to the ssh keys directory"
    )
    args = parser.parse_args()
    scripts.run(setup, LOGGER, "Failed to setup SSH", args.keys)
