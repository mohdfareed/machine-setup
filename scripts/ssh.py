"""SSH setup module."""

import logging
import os
import shutil
from dataclasses import dataclass

import config
import utils
from scripts.package_managers import APT
from utils import shell

LOGGER = logging.getLogger(__name__)
"""The SSH setup logger."""

SSH_DIR: str = os.path.join(os.path.expanduser("~"), ".ssh")
"""The path to the SSH directory."""
PUBLIC_EXT: str = ".pub"
"""The extension of the public key filenames."""
PRIVATE_EXT: str = ".key"
"""The extension of the private key filenames."""


def setup(ssh_config: str | None, ssh_keys=config.ssh_keys) -> None:
    """Setup ssh keys and configuration on a new machine. The ssh keys and
    config file are copied from the specified directory."""

    LOGGER.info("Setting up SSH...")

    if ssh_config:  # symlink ssh config file
        utils.symlink(ssh_config, os.path.join(SSH_DIR, "config"))

    if not os.path.exists(ssh_keys): # check if ssh keys directory exists
        LOGGER.warning("SSH keys directory does not exist: %s", ssh_keys)
        LOGGER.info("Skipping SSH keys setup.")
        return

    # read ssh keys from directory
    for key in _load_keys(ssh_keys):
        _setup_key(key) # setup ssh keys
    LOGGER.info("SSH setup complete")


def _load_keys(keys_dir: str) -> list["_SSHKeyPair"]:
    """Load ssh keys from the specified directory.

    Returns:
        dict[str, SSHKey]: A dict of key names to key pairs.
    """
    keys_dir = os.path.abspath(keys_dir)
    files = os.listdir(keys_dir)  # list of files in the directory

    # load private keys
    private_keys = [
        _SSHKeyPair(private=os.path.join(keys_dir, filename))
        for filename in files
        if filename.endswith(PRIVATE_EXT)
    ]

    # load public keys
    for key in private_keys:
        if key.public_filename in files:
            key.public = os.path.join(keys_dir, key.name + PUBLIC_EXT)

    LOGGER.debug("Loaded %d ssh keys.", len(private_keys))
    return private_keys


def _setup_key(key: "_SSHKeyPair") -> None:
    """Setup an ssh key on a machine."""
    LOGGER.info("Setting up SSH key: %s", key.name)

    # symlink private key and set permissions
    utils.symlink(key.private, os.path.join(SSH_DIR, key.private_filename))
    _set_permissions(key.private, private=True)

    if key.public:  # symlink public key if it exists and set permissions
        utils.symlink(key.public, os.path.join(SSH_DIR, key.public_filename))
        _set_permissions(key.public, private=False)

    # get key fingerprint
    fingerprint = shell.run(f"ssh-keygen -lf {key.private}")[1]
    fingerprint = fingerprint.split(" ")[1]
    LOGGER.debug("Key fingerprint: %s", fingerprint)

    if utils.is_windows():  # set up ssh agent on windows
        shell.run("Get-Service ssh-agent | Set-Service -StartupType Automatic")
        shell.run("Start-Service ssh-agent")
        cmd = f"ssh-add -l | Select-String -Pattern '{fingerprint}'"
    else: # command to check if key already exists in ssh agent
        cmd = "ssh-add -l | grep -q " + fingerprint

    # add key to ssh agent if it doesn't exist
    if shell.run(cmd, throws=False)[0] != 0:
        if utils.is_macos(): # add key to keychain on macOS
            shell.run(f"ssh-add --apple-use-keychain '{key.private}'")

        else: # add key to ssh agent on other operating systems
            shell.run(f"ssh-add '{key.private}'")
        LOGGER.info("Added key to SSH agent")
    else:
        LOGGER.info("Key already exists in SSH agent")


def _set_permissions(filepath: str, private: bool) -> None:
    """Set file permissions based on the operating system."""
    if utils.is_windows():
        shell.run(
            f"icacls {filepath} /inheritance:r /grant:r "
            f"{os.getlogin()}:{"F" if private else "R"}"
        )
    else:
        os.chmod(filepath, 0o600 if private else 0o644)


def setup_server(apt: APT | None) -> None:
    """setup an ssh server on a new machine."""
    LOGGER.info("Setting up SSH server...")

    if utils.is_windows():
        utils.shell.run("Add-WindowsCapability -Online -Name OpenSSH.Server")
        utils.shell.run(
            "Get-Service -Name sshd | Set-Service -StartupType Automatic"
        )
        utils.shell.run("Start-Service sshd")
        LOGGER.debug("SSH server setup complete.")
        return

    if utils.is_macos():
        utils.shell.run("sudo systemsetup -setremotelogin on")
        LOGGER.debug("SSH server setup complete.")
        return

    if utils.is_linux() and apt:
        apt.install("openssh-server")
        utils.shell.run("sudo systemctl start ssh")
        utils.shell.run("sudo systemctl enable ssh")
        LOGGER.debug("SSH server setup complete.")
        return

    if utils.is_linux():
        raise utils.SetupError(
            "APT package manager is required for linux setup."
        )
    raise utils.UnsupportedOS(f"Unsupported operating system: {utils.OS}")

def generate_key_pair(
    name: str,
    keys_dir: str=config.ssh_keys,
    email='mohdf.fareed@icloud.com',
    passphrase=''
) -> None:
    """Create a new ssh key pair."""
    LOGGER.info("Creating SSH key pair: %s", name)

    # ensure keys directory exists
    keys_dir = os.path.abspath(keys_dir)
    if not os.path.exists(keys_dir):
        os.makedirs(keys_dir)

    # define key paths
    private_key=os.path.join(keys_dir, name + PRIVATE_EXT)
    public_key=os.path.join(keys_dir, name + PUBLIC_EXT)

    # check if private key already exists
    if os.path.exists(private_key):
        LOGGER.warning("Private key already exists: %s", private_key)

        if not os.path.exists(public_key): # regenerate public key
            shell.run(f"ssh-keygen -y -f {private_key} > {public_key}")
            LOGGER.info("Public key regenerated: %s", public_key)
        return  # don't overwrite existing key pair

    # overwrite public key if private key doesn't exists
    if os.path.exists(public_key):
        utils.delete(public_key)

    # generate new key pair
    LOGGER.debug("Generating new key pair...")
    key_args = f"-C '{email}' -f {private_key} -N '{passphrase}'"
    shell.run(f"ssh-keygen -t ed25519 {key_args}")
    shutil.move(private_key + ".pub", public_key)

    LOGGER.info("SSH key pair generated: %s", name)
    if os.path.exists(public_key):
        LOGGER.debug("Public key: %s", public_key)
    LOGGER.debug("Private key: %s", private_key)

@dataclass
class _SSHKeyPair:
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
        return self.name + PUBLIC_EXT

    @property
    def name(self) -> str:
        """The name of the key pair based on the private key filename."""
        return os.path.splitext(self.private_filename)[0]



if __name__ == "__main__":
    utils.PARSER.add_argument(
        "ssh_config",
        metavar="SSH_CONFIG",
        help="The path to a SSH configuration file.",
    )
    args = utils.startup(description="SSH setup script.")
    utils.execute(setup, args.ssh_config)
