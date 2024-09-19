"""Setup module containing a `setup` function for setting up macOS."""

__all__ = ["setup"]

import config
import scripts
import utils
from machines import LOGGER, gleason, windows
from scripts import package_managers


def setup() -> None:
    """Setup Gleason config on a new machine."""
    LOGGER.info("Setting up Gleason machine...")
    utils.shell.run("wsl --install", info=True)

    # setup package managers
    winget = package_managers.WinGet()
    scoop = package_managers.Scoop()

    # setup shell
    scripts.shell.setup_windows(windows.ps_profile)
    scripts.shell.install_powershell(winget)
    scripts.shell.install_nvim(winget)
    scripts.shell.install_btop(scoop)

    # setup core machine
    scripts.git.setup(winget, gleason.gitconfig)
    scripts.vscode.setup(winget)
    scoop.setup_fonts()

    # setup dev tools
    scripts.setup_docker(winget)
    scripts.setup_python(scoop)
    scripts.setup_node(None)
    winget.install("GoLang.Go")
    winget.install("Microsoft.DotNet.SDK")
    windows.setup_wsl(gleason.wsl)  # install wsl

    LOGGER.info("Gleason machine setup complete.")
    LOGGER.warning("Restart for some changes to apply.")


if __name__ == "__main__":
    args = utils.startup(description="Gleason machine setup script.")
    config.report(None)
    utils.execute(setup)
