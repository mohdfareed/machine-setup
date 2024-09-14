"""Setup module containing a `setup` function for setting up macOS."""

import config
import scripts
import utils
from machines import LOGGER, gleason, windows
from scripts import git, shell, vscode
from scripts.package_managers import Scoop, WinGet


def setup() -> None:
    """Setup Gleason config on a new machine."""
    LOGGER.info("Setting up Gleason machine...")
    utils.shell.run("wsl --install", info=True)

    # setup package managers
    winget = WinGet()
    scoop = Scoop()

    # setup shell
    shell.setup_windows(windows.ps_profile)
    shell.install_powershell(winget)
    shell.install_nvim(winget)
    shell.install_btop(scoop)

    # setup core machine
    git.setup(winget, gleason.gitconfig)
    vscode.setup(winget)
    scoop.setup_fonts()

    # setup dev tools
    scripts.setup_docker(winget)
    scripts.setup_python(scoop)
    scripts.setup_node(None)
    winget.install("GoLang.Go")
    winget.install("Microsoft.DotNet.SDK")
    windows.setup_wsl("machines.gleason.wsl")  # install wsl

    LOGGER.info("Gleason machine setup complete.")
    LOGGER.warning("Restart for some changes to apply.")


if __name__ == "__main__":
    args = utils.startup(description="Gleason machine setup script.")
    config.report(None)
    utils.execute(setup)
