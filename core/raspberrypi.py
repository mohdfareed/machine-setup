"""Setup module containing a `setup` function for setting up the shell on a new
machine."""

import os
import re

import config
import utils

HOSTNAME = "raspberrypi.local"
"""The local hostname of the Raspberry Pi."""
SETUP_SCRIPT = "setup-machine"
"""The name of the setup script on the Raspberry Pi."""

printer = utils.Printer("raspberrypi")
"""The Raspberry Pi setup printer."""
shell = utils.Shell(printer.debug, printer.error)
"""The Raspberry Pi shell instance."""


def setup(hostname=HOSTNAME) -> None:
    """Setup a Raspberry Pi remotely. This function assumes that the Raspberry
    Pi is connected to the same network as the machine running this script and
    that the Raspberry Pi is accessible via SSH.

    Args:
        hostname (str, optional): The hostname of the Raspberry Pi.
    """
    printer.info("Setting up Raspberry Pi...")

    machine_path = load_zshenv()
    connect(hostname)
    copy_config(hostname, machine_path)
    setup_scripts(hostname, machine_path)
    printer.success("Raspberry Pi setup complete")


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
    printer.print("Connecting to Raspberry Pi...")

    # check if raspberrypi exists
    if shell(["ping", hostname, "-c", "1"], silent=True)[1] != 0:
        raise RuntimeError("Raspberry Pi is not connected to the network")
    printer.debug("Connection to Raspberry Pi established")

    # add ssh key to raspberrypi
    shell(f"ssh-copy-id '{hostname}' > /dev/null 2>&1")
    printer.debug("Added SSH key to Raspberry Pi")


def copy_config(hostname, machine):
    printer.print("Copying config files to Raspberry Pi...")
    shell(["ssh", hostname, "mkdir", "-p", machine], silent=True, safe=True)

    # copy config files to raspberrypi
    machine = f"{hostname}:{machine}"
    shell(["rsync", "-avzL", config.pi_machine + "/", machine], silent=True)
    printer.debug(
        f"Copied: {os.path.basename(config.pi_machine)}/* -> {machine}"
    )

    # copy shared config files
    for config_file in config.pi_shared_config:
        shell(["rsync", "-avzL", config_file, machine], silent=True)
        printer.debug(f"Copied: {os.path.basename(config_file)} -> {machine}")
    printer.debug("Copied config files to Raspberry Pi")


def setup_scripts(hostname, machine):
    printer.print("Setting up scripts on Raspberry Pi...")

    # make scripts executable
    scripts = f"{machine}/scripts"
    shell(["ssh", hostname, "chmod", "+x", f"{scripts}/*.sh"], silent=True)
    printer.debug("Changed scripts to executable")

    # add setup script to path
    setup = f"{scripts}/setup.sh"
    script = f"/usr/local/bin/{SETUP_SCRIPT}"
    shell(["ssh", hostname, "sudo", "ln", "-sf", setup, script], silent=True)
    printer.debug(f"Symlinked: {setup} -> {script}")
    printer.debug("Added setup script to path")
    printer.info(f"Setup Raspberry Pi by executing:[/] [green]{SETUP_SCRIPT}")


if __name__ == "__main__":
    import argparse

    import core

    parser = argparse.ArgumentParser(description="Raspberry Pi setup script.")
    parser.add_argument(
        "hostname", type=str, help="local hostname of Raspberry Pi", nargs="?"
    )
    args = parser.parse_args()
    core.run(
        setup,
        printer,
        "Failed to setup Raspberry Pi",
        args.hostname or HOSTNAME,
    )
