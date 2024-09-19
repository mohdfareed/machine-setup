"""Setup module containing a `setup` function for setting up Windows."""

__all__ = ["setup"]

from typing import Optional

import config
import scripts
import utils
from machines import LOGGER, windows
from scripts import package_managers

from . import setup_wsl


def setup(private_machine: Optional[str] = None) -> None:
    """Setup Windows on a new machine."""
    LOGGER.info("Setting up Windows...")

    # load private machine configuration if provided
    if private_machine:
        config.link_private_config(private_machine)

    # setup package managers
    winget = package_managers.WinGet()
    scoop = package_managers.Scoop()

    # setup shell
    scripts.shell.setup_windows(windows.ps_profile)
    scripts.shell.install_powershell(winget)
    scripts.shell.install_nvim(winget)
    scripts.shell.install_btop(scoop)

    # setup ssh
    scripts.ssh.generate_key_pair("personal")
    scripts.ssh.setup(windows.ssh_config)
    scripts.ssh.setup_server(None)

    # setup core machine
    scripts.git.setup(winget)
    scripts.vscode.setup(winget)
    scripts.vscode.setup_tunnels("pc")
    scripts.tailscale.setup(None)
    scoop.setup_fonts()

    # setup dev tools
    scripts.setup_docker(winget)
    scripts.setup_python(scoop)
    scripts.setup_node(winget)
    winget.install("GoLang.Go")
    winget.install("Microsoft.DotNet.SDK")
    setup_wsl(windows.wsl)  # install ubuntu wsl

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
