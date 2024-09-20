"""Setup module containing a `setup` function for setting up a codespace."""

import config
import scripts
import utils
from machines import codespaces
from scripts import package_managers


def setup() -> None:
    """Setup a new GitHub codespace."""
    apt = package_managers.APT()  # package managers

    # setup core tools
    scripts.git.setup(apt)
    scripts.shell.setup(apt, zshrc=codespaces.zshrc)
    scripts.tools.setup_fonts(apt)

    # set zsh as the default shell
    cmd = 'sudo chsh "$(id -un)" --shell "/usr/bin/zsh"'
    utils.shell.run(cmd, throws=False)


if __name__ == "__main__":
    utils.startup()
    config.report(None)
    setup()
