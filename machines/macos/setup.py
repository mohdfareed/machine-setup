"""Setup module containing a `setup` function for setting up macOS."""

__all__ = ["setup"]

import os
from typing import Optional

import config
import scripts
import utils
from machines import LOGGER, macos
from scripts import package_managers

PAM_SUDO = os.path.join("/", "etc", "pam.d", "sudo_local")
"""The path to the sudo PAM configuration file on macOS."""
PAM_SUDO_MODULE = "pam_tid.so"
"""The name of the PAM module to enable Touch ID for sudo."""
PAM_SUDO_CONTENT = f"""
auth       sufficient     {PAM_SUDO_MODULE}
"""
"""The content to add to the sudo PAM configuration file to enable Touch ID."""


def setup(private_machine: Optional[str] = None) -> None:
    """Setup macOS on a new machine."""
    LOGGER.info("Setting up macOS...")

    # load private machine configuration if provided
    if private_machine:
        config.link_private_config(private_machine)

    LOGGER.info("Authenticate to accept Xcode license.")
    try:  # ensure xcode license is accepted
        utils.shell.run("sudo xcodebuild -license accept", info=True)
    except utils.shell.ShellError as ex:
        raise utils.SetupError(
            "Failed to accept Xcode license. "
            "Ensure Xcode is installed using: xcode-select --install"
        ) from ex

    # setup package managers
    brew = package_managers.HomeBrew()
    package_managers.MAS(brew)

    # setup shell
    scripts.shell.setup(brew, macos.zshrc, macos.zshenv)
    scripts.shell.install_nvim(brew)
    scripts.shell.install_btop(brew)

    # setup ssh
    scripts.ssh.setup(macos.ssh_config)
    scripts.ssh.setup_server(None)

    # setup core machine
    scripts.git.setup(brew)
    scripts.vscode.setup(brew)
    scripts.tailscale.setup(brew)
    scripts.tools.setup(brew)
    # scripts.brew.install_brewfile(macos.brewfile)

    # setup dev tools
    scripts.shell.install_powershell(brew)
    scripts.setup_python(brew)
    scripts.setup_node(brew)
    # scripts.setup_docker(brew)
    brew.install("go")
    brew.install("dotnet-sdk", cask=True)
    brew.install("godot-mono", cask=True)

    # setup system preferences
    LOGGER.debug("Setting system preferences...")
    utils.shell.run(f". {macos.preferences}")
    enable_touch_id()

    LOGGER.info("macOS setup complete.")
    LOGGER.warning("Restart for some changes to apply.")


def enable_touch_id() -> None:
    """Enable Touch ID for sudo on macOS."""
    LOGGER.info("Enabling Touch ID for sudo...")
    with open(PAM_SUDO, "r", encoding="utf-8") as f:
        lines = f.read()

    if PAM_SUDO_MODULE not in lines:
        with open(PAM_SUDO, "a", encoding="utf-8") as f:
            f.write(PAM_SUDO_CONTENT)
        LOGGER.info("Touch ID for sudo enabled.")

    else:
        LOGGER.info("Touch ID for sudo already enabled.")


if __name__ == "__main__":
    utils.PARSER.add_argument(
        "private_machine",
        metavar="PRIVATE_MACHINE",
        nargs="?",
        help="The path to a private machine configuration directory.",
        default=None,
    )
    args = utils.startup(description="macOS setup script.")
    config.report(None)
    utils.execute(setup, args.private_machine)
