"""Setup module containing a `setup` function for setting up the shell on a new
machine.
"""

import config
import utils

ZPROFILE: str = utils.abspath("~/.zprofile", resolve_links=False)
"""The path to the zsh profile file symlink."""
ZSHRC: str = utils.abspath("~/.zshrc", resolve_links=False)
"""The path to the zsh configuration file symlink."""
ZSHENV: str = utils.abspath("~/.zshenv", resolve_links=False)
"""The path to the zsh environment file symlink."""

printer = utils.Printer("shell")
"""The ZSH setup printer."""
shell = utils.Shell(printer.debug, printer.error)
"""The ZSH shell instance."""


def setup() -> None:
    """Setup the shell environment on a machine."""
    printer.info("Setting up shell...")

    # check if homebrew is installed
    if shell(["command", "-v", "brew"], silent=True)[1] != 0:
        raise RuntimeError("Could not find Homebrew")

    # install omz and symlink config files
    install_omz()
    utils.symlink(config.zshrc, ZSHRC)
    utils.symlink(config.zshenv, ZSHENV)
    utils.symlink(config.zprofile, ZPROFILE)
    printer.success("Shell setup complete")


def install_omz():
    printer.info("Installing oh-my-zsh...")

    # load installation environment
    cmd = f"source {config.zsh_env} > /dev/null && echo $ZSH"
    env = dict(ZSH=shell(cmd, silent=True)[0])

    # install oh-my-zsh
    shell(["rm", "-rf", env["ZSH"]], silent=True)
    cmd = '"$(curl -fsSL https://git.io/JvzfK)" "" --unattended'
    if shell(f"sh -c {cmd}", silent=True, env=env)[1] != 0:
        raise RuntimeError("Failed to install oh-my-zsh")
    printer.debug("Installed oh-my-zsh")


if __name__ == "__main__":
    import argparse

    import core

    parser = argparse.ArgumentParser(description="Shell setup script.")
    args = parser.parse_args()
    core.run(setup, printer, "Failed to setup shell")
