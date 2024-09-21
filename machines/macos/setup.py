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
""".strip()


@utils.machine_setup
def setup() -> None:
    """Setup macOS on a new machine."""

    # setup package managers
    LOGGER.info("Setting up macOS...")
    accept_xcode_license()
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
    brew.install_brewfile(macos.brewfile)

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
    if not os.path.exists(PAM_SUDO):
        os.makedirs(os.path.dirname(PAM_SUDO), exist_ok=True)
        utils.shell.run(f"sudo touch {PAM_SUDO}")

    pam_sudo_contents = utils.shell.run(f"cat {PAM_SUDO}")
    if PAM_SUDO_MODULE in pam_sudo_contents:
        LOGGER.info("Touch ID for sudo already enabled.")
        return

    utils.shell.run(f"echo '{PAM_SUDO_CONTENT}' | sudo tee {PAM_SUDO} > /dev/null")
    LOGGER.info("Touch ID for sudo enabled.")


def accept_xcode_license() -> None:
    """Accept the Xcode license."""
    LOGGER.info("Authenticate to accept Xcode license.")
    try:  # ensure xcode license is accepted
        utils.shell.run("sudo xcodebuild -license accept", info=True)
    except utils.shell.ShellError as ex:
        raise utils.SetupError(
            "Failed to accept Xcode license. "
            "Ensure Xcode is installed using: xcode-select --install"
        ) from ex


if __name__ == "__main__":
    utils.startup()
    config.report(None)
    setup()
