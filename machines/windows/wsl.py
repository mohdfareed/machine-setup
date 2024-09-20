"""Setup module containing a `setup` function for setting up WSL."""

__all__ = ["setup"]

import config
import scripts
import utils
from scripts import package_managers


@utils.machine_setup
def setup() -> None:
    """Setup WSL on a new Windows machine."""

    # package managers
    brew = package_managers.HomeBrew.safe_setup()
    apt = package_managers.APT()
    snap = package_managers.SnapStore(apt)

    # setup core machine
    scripts.shell.setup(brew or apt)
    scripts.tools.install_nvim(brew or snap)
    scripts.tools.install_btop(brew or snap)
    scripts.git.setup(brew or apt)
    scripts.tools.setup_fonts(brew or apt)

    # setup dev tools
    scripts.setup_python(brew or apt)
    scripts.setup_node(brew)


if __name__ == "__main__":
    utils.startup()
    config.report(None)
    setup()
