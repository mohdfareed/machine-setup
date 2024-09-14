"""Setup module containing a `setup` function for setting up APT on a on a new
Debian machine."""

import logging
from typing import override

import utils
from config import LOGGER
from scripts.package_managers import PackageManager

LOGGER = logging.getLogger(__name__)
"""The APT package manager logger."""


class APT(PackageManager):
    """Advanced Package Tool (APT) package manager."""

    def setup_fonts(self) -> None:
        """Setup fonts on a new machine."""
        LOGGER.info("Setting up fonts...")
        self.install("fonts-jetbrains-mono")
        LOGGER.debug("Fonts were setup successfully.")

    @staticmethod
    def add_keyring(keyring: str, repo: str, name: str) -> None:
        """Add a keyring to the apt package manager."""
        APT()

        LOGGER.info("Adding keyring %s to apt...", keyring)
        keyring_path = f"/etc/apt/keyrings/{keyring}"

        utils.shell.run(
            f"""
                (type -p wget >/dev/null || sudo apt-get install wget -y) \
                && sudo mkdir -p -m 755 /etc/apt/keyrings && wget -qO- \
                {keyring} | sudo tee {keyring_path} > /dev/null \
                && sudo chmod go+r {keyring_path} \
                && echo "deb [arch=$(dpkg --print-architecture) \
                signed-by={keyring_path}] {repo}" | \
                sudo tee /etc/apt/sources.list.d/{name}.list > /dev/null \
                && sudo apt update
            """
        )
        LOGGER.debug("Keyring %s was added successfully.", keyring)

    @override
    def install(self, package: str | list[str]) -> None:
        if isinstance(package, str):
            package = package.split()

        for pkg in package:
            LOGGER.info("Installing %s from apt...", pkg)
            utils.shell.run(f"sudo apt install -y {pkg}")
            LOGGER.debug("%s was installed successfully.", pkg)
        utils.shell.run("sudo apt autoremove -y")

    @override
    @staticmethod
    def is_supported() -> bool:
        return utils.is_installed("apt")

    @override
    def _setup(self) -> None:
        LOGGER.info("Setting up Debian apt...")
        utils.shell.run("sudo apt update && sudo apt upgrade -y")
        LOGGER.debug("Debian apt was setup successfully.")


if __name__ == "__main__":
    args = utils.startup(description="APT setup script.")
    utils.execute(APT)
