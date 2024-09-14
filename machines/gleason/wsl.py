"""Setup module containing a `setup` function for setting up WSL for a Gleason
machine."""

import config
import scripts
import utils
from machines import LOGGER, gleason
from scripts import git, shell
from scripts.package_managers import APT, HomeBrew, SnapStore


def setup() -> None:
    """Setup WSL on a new Gleason Windows machine."""
    LOGGER.info("Setting up WSL...")

    # package managers
    brew = HomeBrew.safe_setup()
    apt = APT()
    snap = SnapStore(apt)

    # setup core machine
    git.setup(brew or apt, gitconfig=gleason.gitconfig)
    shell.setup(brew or apt)
    shell.install_nvim(brew or snap)
    shell.install_btop(brew or snap)

    if brew:  # setup fonts
        brew.setup_fonts()
    else:
        apt.setup_fonts()

    # setup dev tools
    scripts.setup_python(brew or apt)
    scripts.setup_node(brew)

    LOGGER.info("Gleason WSL setup complete.")
    LOGGER.warning("Restart for some changes to apply.")


if __name__ == "__main__":
    args = utils.startup(description="Gleason WSL setup script.")
    config.report(None)
    utils.execute(setup)
