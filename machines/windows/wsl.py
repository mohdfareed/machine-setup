"""Setup module containing a `setup` function for setting up WSL."""

import config
import utils
from machines import LOGGER
from scripts import git, shell
from scripts.package_managers import APT, HomeBrew, SnapStore


def setup() -> None:
    """Setup WSL on a new Windows machine."""
    LOGGER.info("Setting up WSL...")

    # package managers
    brew = HomeBrew.safe_setup()
    apt = APT()
    snap = SnapStore(apt)

    # setup core machine
    git.setup(brew or apt)
    shell.setup(brew or apt)
    shell.install_nvim(brew or snap)
    shell.install_btop(brew or snap)

    if brew:  # setup fonts
        brew.setup_fonts()
    else:
        apt.setup_fonts()

    LOGGER.info("Windows WSL setup complete.")
    LOGGER.warning("Restart for some changes to apply.")


if __name__ == "__main__":
    args = utils.startup(description="Windows WSL setup script.")
    config.report(None)
    utils.execute(setup)