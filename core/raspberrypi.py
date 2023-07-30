"""Setup module containing a `setup` function for setting up the shell on a new
machine.
"""

from core import raspberrypi_scripts
from resources import micro_settings
from resources import raspberrypi as raspberrypi_resources
from resources import shell_config
from utils import create_file, shell, symlink
from utils.display import Display

DISPLAY: Display = Display(no_logging=True)
"""The default display for printing messages."""

MACHINE_PATH = "~/machine"
SCRIPTS_PATH = "~/machine/scripts"
HOSTNAME = "raspberrypi"


def setup(display=DISPLAY) -> None:
    """Setup a Raspberry Pi remotely. This function assumes that the Raspberry
    Pi is connected to the same network as the machine running this script and
    that the Raspberry Pi is accessible via SSH.

    Args:
        display (Display, optional): The display for printing messages.
    """
    display.header("Setting up Raspberry Pi...")

    # check if raspberrypi.local exists
    if "unknown host" in shell.read(f"ping {HOSTNAME} -c 1"):
        raise RuntimeError("Raspberry Pi is not connected to the network.")

    # copy resources to raspberrypi
    if shell.run(
        f"scp -rp {raspberrypi_resources} {HOSTNAME}:{MACHINE_PATH} && "
        f"scp -rp {shell_config} {HOSTNAME}:{MACHINE_PATH} && "
        f"scp -rp {micro_settings} {HOSTNAME}:{MACHINE_PATH} && "
        f"scp -rp {raspberrypi_scripts} {HOSTNAME}:{SCRIPTS_PATH} && "
        f"ssh {HOSTNAME} 'chmod +x {SCRIPTS_PATH}/*.sh'",
        display.debug,
        display.error,
    ):
        display.error("Failed to copy resources to Raspberry Pi.")
        return
    display.success("Copied resources to Raspberry Pi.")

    # run setup.sh in raspberrypi
    display.info("Setting up Raspberry Pi...")
    error = shell.run(
        f"ssh {HOSTNAME} '{SCRIPTS_PATH}/setup.sh'",
        display.info,
        display.error,
    )
    if error:
        display.error("Failed to set up Raspberry Pi.")
        return

    display.success("Raspberry Pi setup complete.")


if __name__ == "__main__":
    setup()
