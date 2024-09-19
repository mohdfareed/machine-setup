"""Setup module containing a `setup` function for setting up Windows."""

from typing import Optional

import config
import scripts
import utils
from machines import LOGGER, windows
from scripts import git, shell, ssh, tailscale, vscode
from scripts.package_managers import Scoop, WinGet

# from . import setup_wsl, wsl


def setup(private_machine: Optional[str] = None) -> None:
    """Setup Windows on a new machine."""
    LOGGER.info("Setting up Windows...")

    # load private machine configuration if provided
    if private_machine:
        config.link_private_config(private_machine)

    # setup package managers
    winget = WinGet()
    scoop = Scoop()

    # setup shell
    shell.setup_windows(windows.ps_profile)
    shell.install_powershell(winget)
    shell.install_nvim(winget)
    shell.install_btop(scoop)

    # setup ssh
    ssh.generate_key_pair("personal")
    ssh.setup(windows.ssh_config)
    ssh.setup_server(None)

    # setup core machine
    git.setup(winget)
    vscode.setup(winget)
    vscode.setup_tunnels("pc")
    tailscale.setup(None)
    scoop.setup_fonts()

    # setup dev tools
    scripts.setup_docker(winget)
    scripts.setup_python(scoop)
    scripts.setup_node(winget)
    winget.install("GoLang.Go")
    winget.install("Microsoft.DotNet.SDK")
    # setup_wsl(wsl.setup)  # install ubuntu wsl

    # extras
    scoop.add_bucket("extras")
    scoop.install("extras/godot")

    LOGGER.info("Windows setup complete.")
    LOGGER.warning("Restart for some changes to apply.")


if __name__ == "__main__":
    utils.PARSER.add_argument(
        "private_machine",
        metavar="PRIVATE_MACHINE",
        nargs="?",
        help="The path to a private machine configuration directory.",
        default=None,
    )
    args = utils.startup(description="Windows setup script.")
    config.report(None)
    utils.execute(setup, args.private_machine)
