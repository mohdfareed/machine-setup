"""SSH setup module."""

import logging
import os
from dataclasses import dataclass

import config
import utils

SSH_DIR: str = "~/.ssh/"
"""The path to the SSH directory."""
PK_EXT: str = ".pub"
"""The extension of the public key files. Private keys can have any
extension."""

LOGGER = logging.getLogger(__name__)
"""The SSH setup logger."""


@dataclass
class SSHKeyPair:
    """An SSH key pair of a private and optional public keys."""

    private_key: str
    """The path to the private key file."""
    public_key: str | None = None
    """The path to the public key file."""

    @property
    def name(self) -> str:
        """The name of the key pair based on the private key filename."""
        base = os.path.basename(self.private_key)
        return os.path.splitext(base)[0]


def setup() -> None:
    """Setup ssh keys and configuration on a new machine. The ssh keys and
    config file are copied from the specified directory.
    """

    LOGGER.info("Setting up SSH...")
    utils.symlink(config.ssh_config, os.path.join(SSH_DIR, "config"))
    for key in load_keys(config.ssh_keys):
        setup_key(key)
    LOGGER.info("SSH setup complete")


def load_keys(keys_dir: str) -> list[SSHKeyPair]:
    """Load ssh keys from the specified directory.

    Returns:
        dict[str, SSHKey]: A dict of key names to key pairs.
    """
    keys_dir = os.path.abspath(keys_dir)

    # load keys as dictionary of key names to key pairs
    keys = []
    files = os.listdir(keys_dir)
    for filename in files:
        if filename.endswith(PK_EXT):  # look for private keys
            continue  # skip public keys

        key = SSHKeyPair(private_key=os.path.join(keys_dir, filename))
        if key.name + PK_EXT in files:  # find matching public key
            key.public_key = os.path.join(keys_dir, key.name + PK_EXT)
            keys += [key]  # add key pair to list

    LOGGER.debug("Loaded [bold]%d[/] ssh keys.", len(keys))
    return keys


def setup_key(key: SSHKeyPair) -> None:
    """Setup an ssh key on a machine."""
    LOGGER.info("[bold]Setting up SSH key:[/] %s", key.name)

    # symlink private key and set permissions
    utils.symlink(
        key.private_key,
        os.path.join(SSH_DIR, os.path.basename(key.private_key)),
    )
    os.chmod(key.private_key, 0o600)

    # symlink public key and set permissions
    if key.public_key:
        utils.symlink(
            key.public_key,
            os.path.join(SSH_DIR, os.path.basename(key.public_key)),
        )
        os.chmod(key.public_key, 0o644)

    # get key fingerprint
    fingerprint = utils.run_cmd(["ssh-keygen", "-lf", key.public_key])[1]
    fingerprint = fingerprint.split(" ")[1]
    LOGGER.info("[bold]Key fingerprint:[/] %s", fingerprint)

    # add key to ssh agent if it doesn't exist
    cmd = "ssh-add -l | grep -q " + fingerprint
    if utils.run_cmd(cmd, throws=False)[0] != 0:
        utils.run_cmd(f"ssh-add --apple-use-keychain '{key.private_key}'")
        LOGGER.info("Added key to SSH agent")
    else:
        LOGGER.info("Key already exists in SSH agent")
    LOGGER.info("Key setup complete")


if __name__ == "__main__":
    import argparse

    import scripts

    parser = argparse.ArgumentParser(description="SSH setup script.")
    args = parser.parse_args()
    scripts.run_setup_isolated(setup)
