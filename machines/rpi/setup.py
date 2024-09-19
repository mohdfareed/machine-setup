"""Setup module containing a `setup` function for setting up a RPi."""

__all__ = ["setup"]

from typing import Optional

import config
import scripts
import utils
from machines import LOGGER, rpi
from scripts import package_managers

PACKAGES = ["zsh", "git", "code", "npm", "docker-compose"]


def setup(private_machine: Optional[str] = None) -> None:
    """Setup Raspberry Pi on a new machine."""
    LOGGER.info("Setting up Raspberry Pi...")

    # load private machine configuration if provided
    if private_machine:
        config.link_private_config(private_machine)

    # package managers
    apt = package_managers.APT()
    snap = package_managers.SnapStore(apt)

    # setup shell
    scripts.shell.setup(apt, rpi.zshrc, rpi.zshenv)
    scripts.shell.install_nvim(snap)
    scripts.shell.install_btop(snap)
    scripts.shell.install_powershell(snap)

    # setup ssh
    scripts.ssh.generate_key_pair("personal")
    scripts.ssh.setup(rpi.ssh_config)
    scripts.ssh.setup_server(apt)

    # setup core machine
    scripts.git.setup(apt)
    scripts.vscode.setup(snap)
    scripts.vscode.setup_tunnels("rpi")
    scripts.tailscale.setup(None)
    scripts.tools.setup(apt)

    # setup dev tools
    scripts.setup_docker(None)
    scripts.setup_python(apt)
    scripts.setup_node(None)
    snap.install("go", classic=True)
    snap.install("dotnet-sdk", classic=True)

    # machine-specific setup
    utils.shell.run("sudo loginctl enable-linger $USER", throws=False)  # code server
    utils.shell.run("sudo chsh -s $(which zsh)", throws=False)  # change default shell
    utils.shell.run("sudo touch $HOME/.hushlogin", throws=False)  # remove login message
    utils.shell.run("sudo mkdir -p $HOME/.config", throws=False)  # create config directory

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
