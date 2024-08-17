"""Setup module containing a `setup` function for setting up Git on a new
machine."""

import logging

import config
import macos
import utils
from scripts.brew import setup as brew_setup
from scripts.git import setup as git_setup
from scripts.shell import ZSHENV, ZSHRC
from scripts.shell import setup as shell_setup
from scripts.ssh import setup as ssh_setup

PS_PROFILE = "~/.config/powershell/profile.ps1"
"""The path to the PowerShell profile file."""
VSCODE = "~/Library/Application Support/Code/User"
"""The path to the VSCode user settings directory on macOS."""
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

    # setup core machine
    git_setup()
    brew_setup()
    shell_setup()
    ssh_setup()

    # macos-specific configuration
    brew_setup(macos.brewfile)
    utils.symlink(macos.zshrc, ZSHRC)
    utils.symlink(macos.zshenv, ZSHENV)
    utils.symlink(macos.ps_profile, PS_PROFILE)

    # setup vscode settings
    LOGGER.info("Setting up VSCode...")
    utils.symlink_at(config.vscode_settings, VSCODE)
    utils.symlink_at(config.vscode_keybindings, VSCODE)
    utils.symlink_at(config.vscode_snippets, VSCODE)
    LOGGER.debug("Linked VSCode settings.")

    # run the preferences script
    LOGGER.info("Setting system preferences...")
    utils.run(f". {macos.preferences}")
    LOGGER.debug("System preferences set.")

    # use touch ID for sudo
    LOGGER.info("Setting up Touch ID for sudo...")
    with open(PAM_SUDO, "r", encoding="utf-8") as f:
        lines = f.read()
    if PAM_SUDO_MODULE not in lines:
        with open(PAM_SUDO, "a", encoding="utf-8") as f:
            f.write(PAM_SUDO_CONTENT)
        LOGGER.debug("Touch ID for sudo set up.")
    else:
        LOGGER.debug("Touch ID for sudo already set up.")

    LOGGER.info("macOS setup complete.")


if __name__ == "__main__":
    import argparse

    import scripts

    parser = argparse.ArgumentParser(description="macOS setup script.")
    args = parser.parse_args()
    scripts.run_setup_isolated(setup)
