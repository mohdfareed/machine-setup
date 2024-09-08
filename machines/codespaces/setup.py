"""Setup module containing a `setup` function for setting up a codespace."""

import config
import utils
from machines import LOGGER, codespaces
from scripts import git, shell
from scripts.package_managers import apt, snap


def setup() -> None:
    """Setup a new GitHub codespace."""
    LOGGER.info("Setting up codespace...")

    apt.setup()
    snap.setup()

    git.setup()
    shell.setup(zshrc=codespaces.zshrc)

    # set zsh as the default shell
    cmd = 'sudo chsh "$(id -un)" --shell "/usr/bin/zsh"'
    utils.shell.run(cmd, throws=False)

    LOGGER.info("Codespace setup complete.")


if __name__ == "__main__":
    args = utils.startup(description="Codespaces setup script.")
    config.report(None)
    utils.execute(setup)
