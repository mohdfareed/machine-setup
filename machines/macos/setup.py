"""Setup module containing a `setup` function for setting up macOS."""

__all__ = ["setup"]

import os

import config
import scripts
import utils
from machines import LOGGER, macos
from scripts import package_managers

PAM_SUDO = os.path.join("/", "etc", "pam.d", "sudo_local")
PAM_SUDO_MODULE = "pam_tid.so"
PAM_SUDO_CONTENT = f"""
auth       sufficient     {PAM_SUDO_MODULE}
"""


@utils.machine_setup
def setup() -> None:
    """Setup macOS on a new machine."""
    # LOGGER.info("Authenticate to accept Xcode license.")
    # try:  # ensure xcode license is accepted
    #     utils.shell.run("sudo xcodebuild -license accept", info=True)
    # except utils.shell.ShellError as ex:
    #     raise utils.SetupError(
    #         "Failed to accept Xcode license. "
    #         "Ensure Xcode is installed using: xcode-select --install"
    #     ) from ex

    # setup package managers
    LOGGER.info("Setting up macOS...")
    brew = package_managers.HomeBrew()
    package_managers.MAS(brew)

    # setup shell
    scripts.shell.setup(brew, macos.zshrc, macos.zshenv)
    scripts.tools.install_nvim(brew)
    scripts.tools.install_btop(brew)

    # setup ssh
    scripts.ssh.setup(macos.ssh_config)
    scripts.ssh.setup_server(None)

    # setup core machine
    scripts.git.setup(brew)
    scripts.vscode.setup(brew)
    scripts.tailscale.setup(brew)
    scripts.tools.setup_fonts(brew)
    # scripts.brew.install_brewfile(macos.brewfile)

    # setup dev tools
    scripts.tools.install_powershell(brew)
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


def enable_touch_id() -> None:
    """Enable Touch ID for sudo on macOS."""
    LOGGER.info("Enabling Touch ID for sudo...")
    with open(PAM_SUDO, "r", encoding="utf-8") as f:
        lines = f.read()

    if PAM_SUDO_MODULE in lines:
        LOGGER.info("Touch ID for sudo already enabled.")
        return

    with open(PAM_SUDO, "a", encoding="utf-8") as f:
        f.write(PAM_SUDO_CONTENT)
    LOGGER.info("Touch ID for sudo enabled.")


if __name__ == "__main__":
    utils.startup()
    config.report(None)
    setup()
