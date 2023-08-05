"""Setup module containing a `setup` function for setting up the shell on a new
machine."""

import config
import utils

HOSTNAME = "raspberrypi.local"
"""The local hostname of the Raspberry Pi."""
MACHINE = "~/machine"
"""The path to the machine directory on the Raspberry Pi."""
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

    connect(hostname)
    copy_config(hostname)
    setup_scripts(hostname)
    printer.success("Raspberry Pi setup complete")


def connect(hostname):
    printer.print("Connecting to Raspberry Pi...")

    # check if raspberrypi exists
    if shell(["ping", hostname, "-c", "1"], silent=True)[1] != 0:
        raise RuntimeError("Raspberry Pi is not connected to the network")
    printer.debug("Connection to Raspberry Pi established")

    # add ssh key to raspberrypi
    shell(f"ssh-copy-id '{hostname}' > /dev/null 2>&1")
    printer.debug("Added SSH key to Raspberry Pi")


def copy_config(hostname):
    printer.print("Copying config files to Raspberry Pi...")
    shell(["ssh", hostname, "mkdir", "-p", MACHINE], silent=True, safe=True)

    # copy config files to raspberrypi
    machine = f"{hostname}:{MACHINE}"
    shell(["rsync", "-avzL", config.pi_machine + "/", machine], silent=True)
    printer.debug(f"Copied: {config.pi_machine}/* -> {machine}")

    # copy shared config files
    for config_file in config.pi_shared_config:
        shell(["rsync", "-avzL", config_file, machine], silent=True)
        printer.debug(f"Copied: {config_file} -> {machine}")
    printer.debug("Copied config files to Raspberry Pi")


def setup_scripts(hostname):
    printer.print("Setting up scripts on Raspberry Pi...")

    # make scripts executable
    scripts = f"{MACHINE}/scripts"
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
        "hostname", type=str, help="the local hostname of the Raspberry Pi"
    )
    args = parser.parse_args()
    core.run(setup, printer, "Failed to setup Raspberry Pi", args.hostname)
