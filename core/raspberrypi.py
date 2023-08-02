"""Setup module containing a `setup` function for setting up the shell on a new
machine.
"""

import utils
from config import raspberrypi_config, raspberrypi_zshenv, shell_config, micro_settings

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
    shell = utils.Shell()
    printer.title("Setting up Raspberry Pi...")

    # check if raspberrypi exists
    if "unknown host" in shell(f"ping {hostname} -c 1"):
        raise RuntimeError("Raspberry Pi is not connected to the network.")
    display.verbose("Raspberry Pi is connected to the network.")
    # add ssh key to raspberrypi
    shell.run(f"ssh-copy-id {hostname}", display.debug)
    display.verbose("Added SSH key to Raspberry Pi.")

    cmd = (  # raspberry pi resources
        f"rsync -avz {raspberrypi_resources}/* {hostname}:{MACHINE_PATH} && "
        f"rsync -avz {shell_config} {hostname}:{MACHINE_PATH} && "
        f"rsync -avz {micro_settings} {hostname}:{MACHINE_PATH} && "
        f"rsync -avz {raspberrypi_scripts}/* {hostname}:{SCRIPTS_PATH} && "
        f"ssh {hostname} 'chmod +x {SCRIPTS_PATH}/*.sh'"
    )

    # copy resources to raspberrypi
    if shell.run(cmd, display.debug, display.error):
        display.error("Failed to copy resources to Raspberry Pi.")
        return
    display.verbose("Copied resources to Raspberry Pi.")

    # add scripts to path
    cmd = (
        f"ssh {hostname} 'sudo ln -sf {SCRIPTS_PATH}/setup.sh "
        "/usr/local/bin/setup-machine'"
    )
    if shell.run(cmd, display.debug, display.error):
        display.error("Failed to add scripts to path.")
        return
    display.verbose("Added scripts to path.")

    display.success("Raspberry Pi setup complete.")


if __name__ == "__main__":
    setup()
