"""Setup module containing a `setup` function for setting up Git on a new
machine."""

import config
import utils

GITCONFIG: str = utils.abspath("~/.gitconfig", resolve_links=False)
"""The path to the git configuration file on the machine."""
GITIGNORE: str = utils.abspath("~/.gitignore", resolve_links=False)
"""The path to the git ignore file on the machine."""

printer = utils.Printer("git")
"""The git setup printer."""
shell = utils.Shell(printer.debug, printer.error)
"""The git shell instance."""


def setup() -> None:
    """Setup git on a new machine."""
    printer.info("Setting up git...")

    # symlink configuration file
    utils.symlink(config.gitconfig, GITCONFIG)
    utils.symlink(config.gitignore, GITIGNORE)

    printer.success("Git was setup successfully.")


if __name__ == "__main__":
    setup()
