"""Setup module containing a `setup` function for setting up Git on a new
machine.
"""

import utils

# the path to the ssh config file
_config: str = abspath("~/.ssh/config")
printer = utils.Printer("ssh")
"""SSH setup printer."""


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
        display.verbose("Setting up SSH...")
    display.debug(f"SSH directory: {ssh_dir}")

    # copy config file
    config = abspath(f"{ssh_dir}/config")
    copy(config, _config)

    # set ssh paths
    private_key = abspath(f"{ssh_dir}/id_ed25519")
    public_key = abspath(f"{ssh_dir}/id_ed25519.pub")

    # copy private key
    copy(private_key, _private_key)
    # copy public key
    copy(public_key, _public_key)

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
    if shell.run_quiet(cmd, display.debug) != 0:
        shell.run(f"ssh-add '{_private_key}'", display.print, display.error)
        display.verbose("Added ssh key to ssh agent.")

    display.success("SSH was setup successfully.")


def _setup_key():
    # copy private key
    copy(private_key, _private_key)
    # copy public key
    copy(public_key, _public_key)
    # copy config file
    copy(config, _config)

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
    if shell.run_quiet(cmd, display.debug) != 0:
        shell.run(f"ssh-add '{_private_key}'", display.print, display.error)
        display.verbose("Added ssh key to ssh agent.")


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
