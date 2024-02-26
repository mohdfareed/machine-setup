"""Setup module containing a `setup` function for setting up the shell on a new
machine."""

import logging
import os
import re

import config
import utils

HOSTNAME = "raspberrypi.local"
"""The local hostname of the Raspberry Pi."""
SETUP_SCRIPT = "setup-machine"
"""The name of the setup script on the Raspberry Pi."""

LOGGER = logging.getLogger(__name__)
"""The Raspberry Pi setup logger."""


def setup(hostname=HOSTNAME) -> None:
    """Setup a Raspberry Pi remotely. This function assumes that the Raspberry
    Pi is connected to the same network as the machine running this script and
    that the Raspberry Pi is accessible via SSH.

    Args:
        hostname (str, optional): The hostname of the Raspberry Pi.
    """
    LOGGER.info("Setting up Raspberry Pi...")

    machine_path = load_zshenv()
    connect(hostname)
    copy_config(hostname, machine_path)
    setup_scripts(hostname, machine_path)
    LOGGER.info("Raspberry Pi setup complete")


def load_zshenv():
    # parse file and return MACHINE variable
    env_value = None
    with open(config.pi_zshenv, "r") as file:
        for line in file:
            if match := re.match(r"^(export )?MACHINE=(.*?)$", line):
                env_value = match.group(2).strip()
                break
    if not env_value:  # MACHINE variable must be set
        raise RuntimeError("Failed to load MACHINE variable from zshenv")

    match = re.match(r'([\'"])(.*?)\1', env_value)
    if match:  # the value is quoted
        return match.group(2)
    else:  # the value is not quoted, take everything until ` #`
        return env_value.split(" #")[0].strip()


def connect(hostname):
    LOGGER.info("Connecting to Raspberry Pi...")

    # check if raspberrypi exists
    if utils.run_cmd(["ping", hostname, "-c", "1"])[1] != 0:
        raise RuntimeError("Raspberry Pi is not connected to the network")
    LOGGER.debug("Connection to Raspberry Pi established")

    # add ssh key to raspberrypi
    # FIXME: broken prompts (not visible while loading)
    utils.run_cmd(f"ssh-copy-id '{hostname}' > /dev/null 2>&1")
    LOGGER.debug("Added SSH key to Raspberry Pi")


def copy_config(hostname, machine):
    LOGGER.info("Copying config files to Raspberry Pi...")
    utils.run_cmd(["ssh", hostname, "mkdir", "-p", machine], throws=False)

    # copy config files to raspberrypi
    machine = f"{hostname}:{machine}"
    utils.run_cmd(
        ["rsync", "-avzL", config.pi_machine + "/", machine],
        throws=False,
    )
    LOGGER.debug(
        f"Copied: {os.path.basename(config.pi_machine)}/* -> {machine}"
    )

    # copy shared config files
    for config_file in config.pi_shared_config:
        utils.run_cmd(["rsync", "-avzL", config_file, machine], throws=False)
        LOGGER.debug(f"Copied: {os.path.basename(config_file)} -> {machine}")
    LOGGER.debug("Copied config files to Raspberry Pi")


def setup_scripts(hostname, machine):
    LOGGER.info("Setting up scripts on Raspberry Pi...")

    # make scripts executable
    scripts = f"{machine}/scripts"
    utils.run_cmd(["ssh", hostname, "chmod", "+x", f"{scripts}/*.sh"])
    LOGGER.debug("Changed scripts to executable")

    # add setup script to path
    setup = f"{scripts}/setup.sh"
    script = f"/usr/local/bin/{SETUP_SCRIPT}"
    utils.run_cmd(["ssh", hostname, "sudo", "ln", "-sf", setup, script])
    LOGGER.debug(f"Symlinked: {setup} -> {script}")
    LOGGER.debug("Added setup script to path")
    LOGGER.info(f"Setup Raspberry Pi by executing:[/] [green]{SETUP_SCRIPT}")


if __name__ == "__main__":
    import argparse

    import scripts

    parser = argparse.ArgumentParser(description="Raspberry Pi setup script.")
    parser.add_argument(
        "hostname", type=str, help="local hostname of Raspberry Pi", nargs="?"
    )
    args = parser.parse_args()
    scripts.run_setup(setup, args.hostname or HOSTNAME)
