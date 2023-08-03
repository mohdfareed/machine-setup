"""Setup module containing a `setup` function for setting up the shell on a new
machine."""

import config
import utils

HOSTNAME = "raspberrypi.local"
"""The local hostname of the Raspberry Pi."""
MACHINE_PATH = "~/machine"
"""The path to the machine directory on the Raspberry Pi."""

printer = utils.Printer("raspberrypi")
"""The Raspberry Pi setup printer."""
shell = utils.Shell(printer.debug)
"""The Raspberry Pi shell instance."""


def setup(hostname=HOSTNAME) -> None:
    """Setup a Raspberry Pi remotely. This function assumes that the Raspberry
    Pi is connected to the same network as the machine running this script and
    that the Raspberry Pi is accessible via SSH.

    Args:
        hostname (str, optional): The hostname of the Raspberry Pi.
    """
    printer.info("Setting up Raspberry Pi...")

    connect(hostname)
    copy_config(hostname)
    setup_scripts(hostname)
    printer.success("Raspberry Pi setup complete")


def connect(hostname):
    printer.info("Connecting to Raspberry Pi...")

    # check if raspberrypi exists
    if shell(["ping", hostname, "-c", "1"], silent=True, text=False) != 0:
        raise RuntimeError("Raspberry Pi is not connected to the network")
    printer.debug("Connection to Raspberry Pi established")
    # add ssh key to raspberrypi
    shell(f"sudo ssh-copy-id '{hostname}' > /dev/null 2>&1")
    printer.debug("Added SSH key to Raspberry Pi")


def copy_config(hostname):
    printer.info("Copying config files to Raspberry Pi...")
    # create machine directory
    shell(["ssh", hostname, "mkdir", "-p", MACHINE_PATH], safe=True)

    # copy config files to raspberrypi
    machine = f"{hostname}:{MACHINE_PATH}"
    shell(["rsync", "-avzL", config.pi_machine + "/", machine], silent=True)
    printer.debug(f"Copied: {config.pi_machine}/* -> {machine}")

    # copy shared config files
    for config_file in config.pi_shared_config:
        shell(["rsync", "-avzL", config_file, machine], silent=True)
        printer.debug(f"Copied: {config_file} -> {machine}")
    printer.debug("Copied config files to Raspberry Pi")


def setup_scripts(hostname):
    printer.info("Setting up scripts on Raspberry Pi...")

    # make scripts executable
    scripts = f"{MACHINE_PATH}/scripts"
    shell(["ssh", hostname, "chmod", "+x", f"{scripts}/*.sh"])
    # shell(["ssh", hostname, f"chmod +x {scripts}/*.sh"])
    printer.debug("Changed scripts to executable")

    # add setup script to path
    setup_path = f"{scripts}/setup.sh"
    script_path = "/usr/local/bin/setup-machine"
    shell(["ssh", hostname, "sudo", "ln", "-sf", setup_path, script_path])
    printer.info("Setup Raspberry Pi by executing:[/] [green]setup-machine")


if __name__ == "__main__":
    setup()
