"""Setup module containing a `setup` function for setting up macOS."""

import utils
from machines import LOGGER, load_private_machine, rpi
from scripts import brew, git, shell, ssh, vscode
from utils import shell as shell_utils


def setup(private_machine: str | None = None) -> None:
    """Setup Raspberry Pi on a new machine."""
    LOGGER.info("Setting up Raspberry Pi...")

    # load private machine configuration if provided
    if private_machine:
        load_private_machine(private_machine)

    # setup core machine
    git.setup()
    brew.setup(rpi.brewfile)
    shell.setup(rpi.zshrc, rpi.zshenv)
    ssh.setup()
    vscode.setup()

    # setup docker
    # shell_utils.run("sudo snap enable docker")
    shell_utils.run("sudo addgroup --system docker")
    shell_utils.run("sudo adduser $USER docker")

    # FIXME: fix the following
    #     chsh -s $(which zsh)          # change default shell to zsh
    # sudo touch "$HOME/.hushlogin" # remove login message
    # sudo mkdir -p $HOME/.config   # create config directory

    # TODO: figure installing npm (potential dependency) and docker
    # TODO: update and cleanup apt

    # # update packages
    # sudo apt update
    # sudo apt upgrade -y
    # # vim
    # sudo apt install -y npm
    # # snap store
    # sudo apt install -y snapd
    # sudo snap install core
    # sudo snap refresh
    # # docker
    # sudo snap install docker
    # # clean packages
    # sudo apt autoremove -y

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
    utils.execute(setup)
