"""Setup module containing a `setup` function for setting up macOS."""

__all__ = ["setup"]

import config
import scripts
import utils
from machines import gleason, windows
from scripts import package_managers


@utils.machine_setup
def setup() -> None:
    """Setup Gleason config on a new machine."""
    utils.shell.run("wsl --install", info=True)

    # setup package managers
    winget = package_managers.WinGet()
    scoop = package_managers.Scoop()

    # setup shell
    scripts.shell.setup_windows(windows.ps_profile)
    scripts.tools.install_powershell(winget)
    scripts.tools.install_nvim(winget)
    scripts.tools.install_btop(scoop)

    # setup core machine
    scripts.git.setup(winget, gleason.gitconfig)
    scripts.vscode.setup(winget)
    scripts.tools.setup_fonts(scoop)

    # setup dev tools
    scripts.setup_docker(winget)
    scripts.setup_python(scoop)
    scripts.setup_node(None)
    winget.install("GoLang.Go")
    winget.install("Microsoft.DotNet.SDK")
    windows.setup_wsl(gleason.wsl)  # install wsl


if __name__ == "__main__":
    utils.startup()
    config.report(None)
    setup()
