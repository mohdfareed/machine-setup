"""Setup module containing a `setup` function for setting up WSL for a Gleason machine."""

__all__ = ["setup"]

import config
import core
import scripts
from machines import gleason
from scripts import package_managers


@core.machine_setup
def setup() -> None:
    """Setup WSL on a new Gleason Windows machine."""

    # package managers
    brew = package_managers.HomeBrew.safe_setup()
    apt = package_managers.APT()
    snap = package_managers.SnapStore(apt)

    # setup core machine
    scripts.git.setup(brew or apt, gitconfig=gleason.gitconfig)
    scripts.shell.setup(brew or apt)
    scripts.tools.install_nvim(brew or snap)
    scripts.tools.install_btop(brew or snap)
    scripts.tools.setup_fonts(brew or apt)

    # setup dev tools
    scripts.setup_python(brew or apt)
    scripts.setup_node(brew)


if __name__ == "__main__":
    config.report(None)
    setup()
