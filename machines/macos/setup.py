"""Setup module containing a `setup` function for setting up macOS."""

import logging

import utils
from machines.macos import brewfile, preferences, zshenv, zshrc
from scripts.brew import setup as brew_setup
from scripts.git import setup as git_setup
from scripts.shell import ZSHENV, ZSHRC
from scripts.shell import setup as shell_setup
from scripts.ssh import setup as ssh_setup
from scripts.vscode import setup as vscode_setup
from utils import shell

PAM_SUDO = "/etc/pam.d/sudo_local"
"""The path to the sudo PAM configuration file on macOS."""
PAM_SUDO_MODULE = "pam_tid.so"
"""The name of the PAM module to enable Touch ID for sudo."""
PAM_SUDO_CONTENT = f"""
auth       sufficient     {PAM_SUDO_MODULE}
"""
"""The content to add to the sudo PAM configuration file to enable Touch ID."""

LOGGER = logging.getLogger(__name__)
"""The macOS setup logger."""


def setup() -> None:
    """Setup macOS on a new machine."""
    LOGGER.info("Setting up macOS...")

    prompt = "Authenticate to accept Xcode license agreement: "
    try:  # accept xcode license
        shell.run(
            ["sudo", "--prompt", prompt, "xcodebuild", "-license", "accept"],
            msg="Authenticate to accept Xcode license",
        )
    except shell.ShellError as ex:
        raise utils.SetupError(
            "Failed to accept Xcode license."
            "Ensure Xcode is installed using: xcode-select --install"
        ) from ex

    # setup core machine
    git_setup()
    brew_setup(brewfile)
    shell_setup()
    ssh_setup()
    vscode_setup()

    # shell configuration
    utils.symlink(zshrc, ZSHRC)
    utils.symlink(zshenv, ZSHENV)

    # run the preferences script
    LOGGER.debug("Setting system preferences...")
    shell.run(f". {preferences}")

    # use touch ID for sudo
    LOGGER.debug("Setting up Touch ID for sudo...")
    with open(PAM_SUDO, "r", encoding="utf-8") as f:
        lines = f.read()
    if PAM_SUDO_MODULE not in lines:
        with open(PAM_SUDO, "a", encoding="utf-8") as f:
            f.write(PAM_SUDO_CONTENT)
        LOGGER.debug("Touch ID for sudo set up.")
    else:
        LOGGER.debug("Touch ID for sudo already set up.")

    LOGGER.info("macOS setup complete.")
    LOGGER.warning("Restart for some changes to apply.")


if __name__ == "__main__":
    args = utils.startup(description="macOS setup script.")
    utils.execute(setup)
