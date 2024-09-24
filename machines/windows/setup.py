"""Setup module containing a `setup` function for setting up Windows."""

__all__ = ["setup"]

import config
import core
import scripts
from machines import windows
from scripts import package_managers

from . import setup_wsl


@core.machine_setup
def setup() -> None:
    """Setup Windows on a new machine."""

    # setup package managers
    winget = package_managers.WinGet()
    scoop = package_managers.Scoop()

    # setup shell
    scripts.shell.setup_windows(windows.ps_profile)
    scripts.tools.install_powershell(winget)
    scripts.tools.install_nvim(winget)
    scripts.tools.install_btop(scoop)

    # setup ssh
    scripts.ssh.generate_key_pair("personal")
    scripts.ssh.setup(windows.ssh_config)
    scripts.ssh.setup_server(None)

    # setup core machine
    scripts.git.setup(winget)
    scripts.vscode.setup(winget)
    scripts.vscode.setup_tunnels("pc")
    scripts.tailscale.setup(None)
    scripts.tools.setup_fonts(scoop)

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


if __name__ == "__main__":
    config.report(None)
    setup()
