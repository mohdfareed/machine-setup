"""Setup module containing a `setup` function for setting up macOS."""

import config
import scripts
import utils
from machines import LOGGER, gleason, windows
from scripts import git, shell, vscode
from scripts.package_managers import scoop, winget


def setup() -> None:
    """Setup Gleason config on a new machine."""
    LOGGER.info("Setting up Gleason machine...")
    utils.shell.run("wsl --install", info=True)

    # setup winget and scoop
    winget.setup()
    scoop.setup()
    scoop.setup_fonts()

    # setup core machine
    git.setup(gleason.gitconfig)
    shell.setup_windows(windows.ps_profile)
    vscode.setup()

    # setup dev tools
    scripts.setup_docker()
    scripts.setup_python()
    scripts.setup_node()
    winget.install("GoLang.Go")
    winget.install("Microsoft.DotNet.SDK")
    windows.setup_wsl("machines.gleason.wsl")  # install wsl

    LOGGER.info("Gleason machine setup complete.")
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
