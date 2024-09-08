"""Setup module containing a `setup` function for setting up Windows."""

import config
import scripts
import utils
from machines import LOGGER, windows
from scripts import git, shell, ssh, tailscale, vscode
from scripts.package_managers import scoop, winget


def setup(private_machine: str | None = None) -> None:
    """Setup Windows on a new machine."""
    LOGGER.info("Setting up Windows...")

    # load private machine configuration if provided
    if private_machine:
        config.link_private_config(private_machine)

    # setup winget and scoop
    winget.setup()
    scoop.setup()
    scoop.setup_fonts()

    # setup core machine
    git.setup()
    shell.setup_windows(windows.ps_profile)
    ssh.setup(windows.ssh_config)
    ssh.setup_server()
    vscode.setup()
    vscode.setup_tunnels("pc")
    tailscale.setup()

    # setup dev tools
    scripts.setup_docker()
    scripts.setup_python()
    scripts.setup_node()
    winget.install("GitHub.cli")
    winget.install("GoLang.Go")
    winget.install("Microsoft.DotNet.SDK")
    scoop.install("extras/godot")
    setup_wsl()  # install wsl

    LOGGER.info("Windows setup complete.")
    LOGGER.warning("Restart for some changes to apply.")


def setup_wsl(wsl_module="machines.windows.wsl") -> None:
    """Setup WSL on a new machine."""
    LOGGER.info("Setting up WSL...")
    utils.shell.run("wsl --install", info=True)

    wsl_commands = (
        f"cd {config.MACHINE} && ",
        f"python -m {wsl_module}",
    )
    utils.shell.run(f'wsl -e bash -c "{wsl_commands}"', info=True)
    LOGGER.info("WSL setup complete.")


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
