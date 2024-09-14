"""Setup module containing a `setup` function for setting up macOS."""

import config
import scripts
import utils
from machines import LOGGER, rpi
from scripts import git, shell, ssh, tailscale, vscode
from scripts.package_managers import APT, SnapStore
from utils import shell as shell_utils

PACKAGES = ["zsh", "git", "code", "npm", "docker-compose"]


def setup(private_machine: str | None = None) -> None:
    """Setup Raspberry Pi on a new machine."""
    LOGGER.info("Setting up Raspberry Pi...")

    # load private machine configuration if provided
    if private_machine:
        config.link_private_config(private_machine)

    # package managers
    apt = APT()
    snap = SnapStore(apt)

    # setup shell
    shell.setup(apt, rpi.zshrc, rpi.zshenv)
    shell.install_nvim(snap)
    shell.install_btop(snap)
    shell.install_powershell(snap)

    # setup core machine
    git.setup(apt)
    vscode.setup(snap)
    vscode.setup_tunnels("rpi")
    tailscale.setup(None)
    ssh.setup_server(apt)
    apt.setup_fonts()

    # setup dev tools
    scripts.setup_docker(None)
    scripts.setup_python(apt)
    scripts.setup_node(None)
    snap.install("go", classic=True)
    snap.install("dotnet-sdk", classic=True)

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
