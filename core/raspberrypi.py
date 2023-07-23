"""Setup module containing a `setup` function for setting up the shell on a new
machine.
"""

from resources import raspberrypi as raspberrypi_resources
from core import raspberrypi as raspberrypi_core
from utils import create_file, shell, symlink
from utils.display import Display

DISPLAY: Display = Display(no_logging=True)
"""The default display for printing messages."""


def setup(display=DISPLAY) -> None:
    """Setup a Raspberry Pi remotely. This function assumes that the Raspberry
    Pi is connected to the same network as the machine running this script and
    that the Raspberry Pi is accessible via SSH.

    Args:
        display (Display, optional): The display for printing messages.
    """
    display.header("Setting up Raspberry Pi...")

    # check if raspberrypi.localhost exists
    # prompt for hostname if it doesn't
    # set hostname to raspberrypi.localhost
    # ssh into raspberrypi.localhost
    # copy resources to raspberrypi
    # run setup.sh in raspberrypi

    display.success("Raspberry Pi setup complete")


if __name__ == "__main__":
    setup()
