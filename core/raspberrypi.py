"""Setup module containing a `setup` function for setting up the shell on a new
machine.
"""

import config
import utils

HOSTNAME = "raspberrypi.local"
"""The local hostname of the Raspberry Pi."""

printer = utils.Printer("raspberrypi")
"""the main setup printer."""


def setup(hostname=HOSTNAME) -> None:
    """Setup a Raspberry Pi remotely. This function assumes that the Raspberry
    Pi is connected to the same network as the machine running this script and
    that the Raspberry Pi is accessible via SSH.

    Args:
        hostname (str, optional): The hostname of the Raspberry Pi.
    """
    shell = utils.Shell(printer.debug)
    printer.title("Setting up Raspberry Pi...")

    # check if raspberrypi exists
    if shell(["ping", hostname, "-c", 1], safe=True) != 0:
        raise RuntimeError("Raspberry Pi is not connected to the network")
    printer.debug("Raspberry Pi is connected to the network")
    # add ssh key to raspberrypi
    shell(f"ssh-copy-id {hostname}")
    printer.debug("Added SSH key to Raspberry Pi")

    shell(["ssh", hostname, "mkdir", "-p", config.MACHINE_PATH])

    cmd = (  # raspberry pi resources
        f"rsync -avz {config.pi_config}/* {hostname}:{MACHINE_PATH} && "
        f"rsync -avz {shell_config} {hostname}:{MACHINE_PATH} && "
        f"rsync -avz {micro_settings} {hostname}:{MACHINE_PATH} && "
        f"ssh {hostname} 'chmod +x {SCRIPTS_PATH}/*.sh'"
    )

    # copy resources to raspberrypi
    if shell.run(cmd, display.debug, display.error):
        display.error("Failed to copy resources to Raspberry Pi.")
        return
    display.verbose("Copied resources to Raspberry Pi.")

    # add scripts to path
    cmd = f"sudo ln -sf ~/machine/setup.sh /usr/local/bin/setup-machine"
    cmd = (
        f"ssh {hostname} 'sudo ln -sf {SCRIPTS_PATH}/setup.sh "
        "/usr/local/bin/setup-machine'"
    )
    if shell.run(cmd, display.debug, display.error):
        display.error("Failed to add scripts to path.")
        return
    display.verbose("Added scripts to path.")

    display.success("Raspberry Pi setup complete.")


def load_machine_path():
    """Load the path to the machine directory on the Raspberry Pi."""
    config_path = utils.abspath(config.pi_config, "z")
    return f"pi@{HOSTNAME}:{config.MACHINE_PATH}"


if __name__ == "__main__":
    setup()
