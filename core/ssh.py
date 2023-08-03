"""SSH setup module."""

import os
from collections import defaultdict

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
shell = utils.Shell(printer.debug)
"""The SSH shell instance."""


class SSHKey:
    def __init__(self) -> None:
        self.private_key: str | None = None
        """The path to the private key file."""
        self.public_key: str | None = None
        """The path to the public key file."""


def setup(config_path: str | None) -> None:
    """Setup ssh keys and configuration on a new machine. The ssh keys and
    config file are copied from the specified directory.

    Args:
        config_path (str): The path to the directory containing the ssh keys.
    """
    printer.info("Setting up SSH...")

    # copy config file
    utils.symlink(config.ssh_config, SSH_DIR + "config")
    # parse ssh keys path
    if not config_path:
        return
    keys = os.path.join(config_path, "keys")

    # setup ssh keys
    key_pairs = load_keys(keys)
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
    printer.print(f"Setting up SSH key: [bold]{name}[/]")
    if not key.private_key or not key.public_key:
        printer.error(f"Invalid ssh key pair:")
        printer.error(f"    Private key: {key.private_key}")
        printer.error(f"    Public key: {key.public_key}")
        raise RuntimeError(f"Invalid ssh key pair encountered: {name}")

    # copy private key and set permissions
    utils.copy(key.private_key, SSH_DIR)
    private_key = os.path.join(SSH_DIR, os.path.basename(key.private_key))
    private_key = utils.abspath(private_key)
    utils.chmod(private_key, 600)

    # copy public key and set permissions
    utils.copy(key.public_key, SSH_DIR)
    public_key = os.path.join(SSH_DIR, os.path.basename(key.public_key))
    public_key = utils.abspath(public_key)
    utils.chmod(public_key, 644)

    # get key fingerprint
    fingerprint = shell(["ssh-keygen", "-lf", public_key], silent=True)[
        0
    ].split(" ")[1]
    printer.print(f"Key fingerprint: [bold]{fingerprint}[/]")

    # add key to ssh agent if it doesn't exist
    cmd = "ssh-add -l | grep -q " + fingerprint
    if shell(cmd, silent=True, text=False) != 0:
        shell(f"ssh-add '{private_key}'")
        printer.print("Added key to SSH agent.")
    else:
        printer.print("Key already added to ssh agent.")
    printer.success("Key setup complete")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SSH setup script.")
    parser.add_argument(
        "--keys", type=str, help="the path to the ssh keys directory"
    )
    args = parser.parse_args()
    setup(args.keys)
