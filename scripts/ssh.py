"""SSH setup module."""

import logging
import os
from dataclasses import dataclass

import config
import utils
from utils import shell

LOGGER = logging.getLogger(__name__)
"""The SSH setup logger."""

SSH_DIR: str = "~/.ssh/"
"""The path to the SSH directory."""
PUBLIC_EXT: str = ".pub"
"""The extension of the public key filenames."""
PRIVATE_EXT: str = ".key"
"""The extension of the private key filenames."""


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
    def public_filename(self) -> str:
        """The filename of the public key, based on the private key if the
        public key doesn't exist."""
        if self.public:
            return os.path.basename(self.public)
        else:
            return self.name + PUBLIC_EXT

    @property
    def name(self) -> str:
        """The name of the key pair based on the private key filename."""
        return os.path.splitext(self.private_filename)[0]


def setup() -> None:
    """Setup ssh keys and configuration on a new machine. The ssh keys and
    config file are copied from the specified directory."""
    LOGGER.info("Setting up SSH...")

    if not os.path.exists(config.ssh_keys):
        LOGGER.error("SSH keys directory does not exist: %s", config.ssh_keys)
        return

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
    files = os.listdir(keys_dir)  # list of files in the directory

    # load private keys
    private_keys = [
        SSHKeyPair(private=os.path.join(keys_dir, filename))
        for filename in files
        if filename.endswith(PRIVATE_EXT)
    ]

    # load public keys
    for key in private_keys:
        if key.public_filename in files:
            key.public = os.path.join(keys_dir, key.name + PUBLIC_EXT)

    LOGGER.debug("Loaded [bold]%d[/] ssh keys.", len(private_keys))
    return private_keys


def setup_key(key: SSHKeyPair) -> None:
    """Setup an ssh key on a machine."""
    LOGGER.info("[bold]Setting up SSH key:[/] %s", key.name)

    # symlink private key and set permissions
    utils.symlink(key.private, os.path.join(SSH_DIR, key.private_filename))
    os.chmod(key.private, 0o600)
    if key.public:  # symlink public key if it exists and set permissions
        utils.symlink(key.public, os.path.join(SSH_DIR, key.public_filename))
        os.chmod(key.public, 0o644)

    # get key fingerprint
    fingerprint = shell.run(f"ssh-keygen -lf {key.private}")[1]
    fingerprint = fingerprint.split(" ")[1]
    LOGGER.debug("[bold]Key fingerprint:[/] %s", fingerprint)

    # add key to ssh agent if it doesn't exist
    cmd = "ssh-add -l | grep -q " + fingerprint
    if shell.run(cmd, throws=False)[0] != 0:
        if not utils.is_macos():
            shell.run(f"ssh-add '{key.private}'")
        else:
            shell.run(f"ssh-add --apple-use-keychain '{key.private}'")
        LOGGER.info("Added key to SSH agent")
    else:
        LOGGER.info("Key already exists in SSH agent")


if __name__ == "__main__":
    args = utils.startup(description="SSH setup script.")
    utils.execute(setup)
