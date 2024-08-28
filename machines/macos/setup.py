"""Setup module containing a `setup` function for setting up macOS."""

import utils
from machines import LOGGER, load_private_machine, macos
from scripts import brew, git, shell, ssh, vscode
from utils import shell as shell_utils

PAM_SUDO = "/etc/pam.d/sudo_local"
"""The path to the sudo PAM configuration file on macOS."""
PAM_SUDO_MODULE = "pam_tid.so"
"""The name of the PAM module to enable Touch ID for sudo."""
PAM_SUDO_CONTENT = f"""
auth       sufficient     {PAM_SUDO_MODULE}
"""
"""The content to add to the sudo PAM configuration file to enable Touch ID."""


def setup(private_machine: str | None = None) -> None:
    """Setup macOS on a new machine."""
    LOGGER.info("Setting up macOS...")

    # load private machine configuration if provided
    if private_machine:
        load_private_machine(private_machine)

    # ensure xcode license is accepted
    prompt = "Authenticate to accept Xcode license agreement: "
    try:  # accept xcode license
        shell_utils.run(
            ["sudo", "--prompt", prompt, "xcodebuild", "-license", "accept"],
            msg="Authenticate to accept Xcode license",
        )
    except shell_utils.ShellError as ex:
        raise utils.SetupError(
            "Failed to accept Xcode license."
            "Ensure Xcode is installed using: xcode-select --install"
        ) from ex

    # setup core machine
    git.setup()
    brew.setup(macos.brewfile)
    shell.setup(macos.zshrc, macos.zshenv)
    ssh.setup()
    vscode.setup()

    # run the preferences script
    LOGGER.debug("Setting system preferences...")
    shell_utils.run(f". {macos.preferences}")

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
    utils.PARSER.add_argument(
        "private_machine",
        metavar="PRIVATE_MACHINE",
        nargs="?",
        help="The path to a private machine configuration directory.",
        default=None,
    )
    args = utils.startup(description="macOS setup script.")
    utils.execute(setup, args.private_machine)
