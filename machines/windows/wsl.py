"""Setup module containing a `setup` function for setting up WSL."""

import config
import scripts
import utils
from machines import LOGGER
from scripts import git, shell
from scripts.package_managers import apt, brew, scoop


def setup() -> None:
    """Setup WSL on a new Windows machine."""
    LOGGER.info("Setting up WSL...")

    try:
        brew.setup()
    except utils.SetupError:
        apt.setup()
        scoop.setup()

    try:
        brew.setup_fonts()
    except utils.SetupError:
        scoop.setup_fonts()

    # setup core machine
    git.setup()
    shell.setup()

    # setup dev tools
    scripts.setup_python()
    scripts.setup_node()

    LOGGER.info("Windows WSL setup complete.")
    LOGGER.warning("Restart for some changes to apply.")


if __name__ == "__main__":
    args = utils.startup(description="Windows WSL setup script.")
    config.report(None)
    utils.execute(setup)
