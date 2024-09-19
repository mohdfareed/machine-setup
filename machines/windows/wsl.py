"""Setup module containing a `setup` function for setting up WSL."""

__all__ = ["setup"]

import config
import scripts
import utils
from machines import LOGGER
from scripts import package_managers


def setup() -> None:
    """Setup WSL on a new Windows machine."""
    LOGGER.info("Setting up WSL...")

    # package managers
    brew = package_managers.HomeBrew.safe_setup()
    apt = package_managers.APT()
    snap = package_managers.SnapStore(apt)

    # setup core machine
    scripts.shell.setup(brew or apt)
    scripts.shell.install_nvim(brew or snap)
    scripts.shell.install_btop(brew or snap)
    scripts.git.setup(brew or apt)
    scripts.tools.setup(brew or apt)

    # setup dev tools
    scripts.setup_python(brew or apt)
    scripts.setup_node(brew)

    LOGGER.info("Windows WSL setup complete.")
    LOGGER.warning("Restart for some changes to apply.")


if __name__ == "__main__":
    args = utils.startup(description="Windows WSL setup script.")
    config.report(None)
    utils.execute(setup)
