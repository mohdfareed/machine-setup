"""Setup module containing a `setup` function for setting up Scoop on a new
Windows machine."""

import logging
from typing import override

import utils
from scripts.package_managers import PackageManager

LOGGER = logging.getLogger(__name__)
"""Scoop package manager logger."""


class Scoop(PackageManager):
    """Scoop package manager."""

    def setup_fonts(self) -> None:
        """Setup fonts on a new machine."""
        LOGGER.info("Setting up fonts...")
        self.install("nerd-fonts/JetBrains-Mono")
        LOGGER.debug("Fonts were setup successfully.")

    @override
    def install(self, package: str | list[str]) -> None:
        if isinstance(package, str):
            package = package.split()

        for pkg in package:
            LOGGER.info("Installing %s with Scoop...", pkg)
            utils.shell.run(f"scoop install {pkg}")
            LOGGER.debug("%s was installed successfully.", pkg)

    @override
    @staticmethod
    def is_supported() -> bool:
        return utils.is_windows()

    @override
    def _setup(self) -> None:
        LOGGER.info("Setting up Scoop...")
        utils.shell.run(
            "Set-ExecutionPolicy -ExecutionPolicy "
            "RemoteSigned -Scope CurrentUser"
        )
        installer = utils.shell.run("New-TemporaryFile")[1]
        utils.shell.run(f"irm get.scoop.sh -OutFile '{installer}'")
        utils.shell.run(f"& '{installer}'")
        utils.shell.run(f"Remove-Item '{installer}'")
        utils.shell.run("scoop update")
        utils.shell.run("scoop update *")
        LOGGER.debug("Scoop was setup successfully.")


if __name__ == "__main__":
    args = utils.startup(description="Scoop setup script.")
    utils.execute(Scoop)
