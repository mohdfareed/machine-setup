"""Setup module containing a `setup` function for setting up macOS."""

import config
import utils
from machines import LOGGER, rpi
from scripts import git, shell, vscode
from utils import shell as shell_utils


def setup(private_machine: str | None = None) -> None:
    """Setup Raspberry Pi on a new machine."""
    LOGGER.info("Setting up Raspberry Pi...")

    # load private machine configuration if provided
    if private_machine:
        config.link_private_config(private_machine)

    # install rpi packages script
    shell_utils.run(rpi.packages)

    # setup core machine
    git.setup()
    shell.setup(rpi.zshrc, rpi.zshenv)
    vscode.setup()
    vscode.setup_tunnels()

    # setup docker
    shell_utils.run("sudo snap enable docker")
    shell_utils.run("sudo addgroup --system docker")
    shell_utils.run("sudo adduser $USER docker")

    # machine-specific setup
    shell_utils.run("chsh -s $(which zsh)")  # set zsh as default shell
    shell_utils.run("sudo touch $HOME/.hushlogin")  # remove login message
    shell_utils.run("sudo mkdir -p $HOME/.config")  # create config directory

    LOGGER.info("Raspberry Pi setup complete.")
    LOGGER.warning("Restart for some changes to apply.")


if __name__ == "__main__":
    utils.PARSER.add_argument(
        "private_machine",
        metavar="PRIVATE_MACHINE",
        nargs="?",
        help="The path to a private machine configuration directory.",
        default=None,
    )
    args = utils.startup(description="Raspberry Pi setup script.")
    config.report(None)
    utils.execute(setup)
