"""SSH setup module."""

import logging
import os
from dataclasses import dataclass

import config
import utils

SSH_DIR: str = "~/.ssh/"
"""The path to the SSH directory."""
PK_EXT: str = ".pub"
"""The extension of the public key files."""

LOGGER = logging.getLogger(__name__)
"""The SSH setup logger."""


@dataclass
class SSHKeyPair:
    """An SSH key pair of a private and optional public keys."""

    private: str
    """The path to the private key file."""
    public: str | None = None
    """The path to the public key file."""

    @property
    def private_filename(self) -> str:
        """The filename of the private key."""
        return os.path.basename(self.private)

    @property
    def public_filename(self) -> str | None:
        """The filename of the public key."""
        return os.path.basename(self.public) if self.public else None

    @property
    def name(self) -> str:
        """The name of the key pair based on the private key filename."""
        base = os.path.basename(self.private)
        return os.path.splitext(base)[0]


def setup(mac=False) -> None:
    """Setup ssh keys and configuration on a new machine. The ssh keys and
    config file are copied from the specified directory.
    """

    LOGGER.info("Setting up SSH...")
    utils.symlink(config.macos_ssh_config, os.path.join(SSH_DIR, "config"))
    for key in load_keys(config.ssh_keys):
        setup_key(key, mac)
    LOGGER.info("SSH setup complete")


def load_keys(keys_dir: str) -> list[SSHKeyPair]:
    """Load ssh keys from the specified directory.

    Returns:
        dict[str, SSHKey]: A dict of key names to key pairs.
    """
    keys_dir = os.path.abspath(keys_dir)
    keys = []  # map of key names to key pairs

    # load keys by finding private keys and matching public keys
    files = os.listdir(keys_dir)
    for filename in files:
        if filename.endswith(PK_EXT):
            continue  # skip public keys

        key = SSHKeyPair(private=os.path.join(keys_dir, filename))
        if key.name + PK_EXT in files:  # find matching public key
            key.public = os.path.join(keys_dir, key.name + PK_EXT)
            keys += [key]  # add key pair to list

    LOGGER.debug("Loaded [bold]%d[/] ssh keys.", len(keys))
    return keys


def setup_key(key: SSHKeyPair, mac: bool) -> None:
    """Setup an ssh key on a machine."""
    LOGGER.info("[bold]Setting up SSH key:[/] %s", key.name)

    # symlink private key and set permissions
    utils.symlink(
        key.private,
        os.path.join(SSH_DIR, key.private_filename),
    )
    os.chmod(key.private, 0o600)

    # symlink public key and set permissions
    if key.public and key.public_filename:
        utils.symlink(
            key.public,
            os.path.join(SSH_DIR, os.path.basename(key.public_filename)),
        )
        os.chmod(key.public, 0o644)

    # get key fingerprint
    fingerprint = utils.run_cmd(["ssh-keygen", "-lf", key.public])[1]
    fingerprint = fingerprint.split(" ")[1]
    LOGGER.info("[bold]Key fingerprint:[/] %s", fingerprint)

    # add key to ssh agent if it doesn't exist
    cmd = "ssh-add -l | grep -q " + fingerprint
    if utils.run_cmd(cmd, throws=False)[0] != 0:
        if not mac:
            utils.run_cmd(f"ssh-add '{key.private}'")
        else:
            utils.run_cmd(f"ssh-add --apple-use-keychain '{key.private}'")
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
