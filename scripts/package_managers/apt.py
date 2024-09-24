"""Setup module containing a `setup` function for setting up APT on a on a new
Debian machine."""

__all__ = ["APT"]

from typing import Union

import utils
from scripts.package_managers.models import LOGGER, PackageManager


class APT(PackageManager):
    """Advanced Package Tool (APT) package manager."""

    @staticmethod
    def add_keyring(keyring: str, repo: str, name: str) -> None:
        """Add a keyring to the apt package manager."""
        APT()

        LOGGER.info("Adding keyring %s to apt...", keyring)
        keyring_path = f"/etc/apt/keyrings/{keyring}"

        utils.shell.execute(
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

    @staticmethod
    def is_supported() -> bool:
        return utils.is_installed("apt")

    @PackageManager.installation
    def install(self, package: Union[str, list[str]]) -> None:
        utils.shell.execute(f"sudo apt install -y {package}")

    def _setup(self) -> None:
        utils.shell.execute("sudo apt update && sudo apt upgrade -y")

    def __del__(self) -> None:
        LOGGER.debug("Cleaning up APT...")
        utils.shell.execute("sudo apt autoremove -y")
        LOGGER.debug("APT cleanup complete.")
