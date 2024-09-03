"""Setup module containing a `setup` function for setting up macOS."""

import config
import utils
from machines import LOGGER, rpi
from scripts import apt, git, shell, tailscale, vscode
from utils import shell as shell_utils

PACKAGES = ["zsh", "git", "code", "npm", "docker-compose"]


def setup(private_machine: str | None = None) -> None:
    """Setup Raspberry Pi on a new machine."""
    LOGGER.info("Setting up Raspberry Pi...")

    # load private machine configuration if provided
    if private_machine:
        config.link_private_config(private_machine)

    # setup core machine
    git.setup()
    shell.setup(rpi.zshrc, rpi.zshenv)
    vscode.setup()
    vscode.setup_tunnels()
    tailscale.setup()

    # setup apt
    apt.setup()
    apt.setup_snap()
    apt.setup_docker()
    apt.setup_python()
    apt.setup_node()
    apt.install_snap("go", classic=True)
    apt.install_snap("dotnet-sdk", classic=True)

    # machine-specific setup
    shell_utils.run(
        "sudo loginctl enable-linger $USER", throws=False
    )  # code server
    shell_utils.run(
        "sudo chsh -s $(which zsh)", throws=False
    )  # change default shell
    shell_utils.run(
        "sudo touch $HOME/.hushlogin", throws=False
    )  # remove login message
    shell_utils.run(
        "sudo mkdir -p $HOME/.config", throws=False
    )  # create config directory

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
