"""Setup module containing a `setup` function for setting up WSL."""

__all__ = ["setup"]

import config
import scripts
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
    shell.setup(brew or apt)
    shell.install_nvim(brew or snap)
    shell.install_btop(brew or snap)
    git.setup(brew or apt)
    scripts.fonts.setup(brew or apt)

    # setup dev tools
    scripts.setup_python(brew or apt)
    scripts.setup_node(brew)

    LOGGER.info("Windows WSL setup complete.")
    LOGGER.warning("Restart for some changes to apply.")


if __name__ == "__main__":
    args = utils.startup(description="Windows WSL setup script.")
    config.report(None)
    utils.execute(setup)
