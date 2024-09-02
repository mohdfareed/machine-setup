"""Setup module containing a `setup` function for setting up macOS."""

import config
import utils
from machines import LOGGER, rpi
from scripts import git, shell, tailscale, vscode
from utils import shell as shell_utils

PACKAGES = ["zsh", "git", "code", "npm", "docker-compose"]


def setup(private_machine: str | None = None) -> None:
    """Setup Raspberry Pi on a new machine."""
    LOGGER.info("Setting up Raspberry Pi...")

    # load private machine configuration if provided
    if private_machine:
        config.link_private_config(private_machine)

    # update packages
    update()
    # install docker
    shell_utils.run("curl -fsSL https://get.docker.com | sh", throws=False)
    # install packages
    install(PACKAGES)

    # setup core machine
    git.setup()
    shell.setup(rpi.zshrc, rpi.zshenv)
    vscode.setup()
    vscode.setup_tunnels()
    tailscale.setup()

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


def update() -> None:
    """Update Raspberry Pi packages."""
    utils.shell.run("sudo apt update && sudo apt upgrade -y")
    utils.shell.run("sudo apt autoremove -y")


def install(packages: list[str]) -> None:
    """Install packages on Raspberry Pi."""
    utils.shell.run(f"sudo apt install -y {' '.join(packages)}")
    utils.shell.run("sudo apt autoremove -y")


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
