"""Setup module containing a `setup` function for setting up Homebrew on a new
machine."""

__all__ = ["HomeBrew"]


import os
from typing import Optional, Union, override

import utils
from scripts.package_managers.models import LOGGER, PackageManager
from utils import shell


class HomeBrew(PackageManager):
    """Homebrew package manager."""

    bin = (
        os.path.join("/", "opt", "homebrew", "bin")
        if utils.is_macos()
        else os.path.join("/", "home", "linuxbrew", ".linuxbrew", "bin")
    )
    """The path to the Homebrew executables."""
    brew = os.path.join(bin, "brew")
    """The path to the brew executable."""

    @classmethod
    def safe_setup(cls) -> "Optional[HomeBrew]":
        """Safely setup Homebrew without throwing exceptions."""

        try:
            return HomeBrew()
        except utils.SetupError as ex:
            LOGGER.error("Homebrew is not supported: %s", ex)
            return None

    @override
    def install(self, package: Union[str, list[str]], cask: bool = False) -> None:
        if isinstance(package, list):
            for p in package:
                super().install(f"{'--cask' if cask else ''} {p}")
        else:
            super().install(f"{'--cask' if cask else ''} {package}")

    @override
    @staticmethod
    def is_supported() -> bool:
        return utils.is_macos() or not utils.is_arm()

    def install_brewfile(self, file: str) -> None:
        """Install Homebrew packages from a Brewfile."""

        LOGGER.info("Installing Homebrew packages from Brewfile...")
        shell.run(f"{self.brew} bundle install --file={file}")
        shell.run(f"{self.brew} cleanup --prune=all", throws=False)
        LOGGER.debug("Homebrew packages were installed successfully.")

    @override
    def _install(self, package: str) -> None:
        shell.run(f"{self.brew} install {package}")

    @override
    def _setup(self) -> None:
        if not os.path.exists(self.brew):
            self._install_brew()
        shell.run(f"{self.brew} update && {self.brew} upgrade")

    def _install_brew(self) -> None:
        LOGGER.info("Installing Homebrew...")
        try:  # install homebrew otherwise
            shell.run('/bin/bash -c "$(curl -fsSL https://git.io/JIY6g)"')
        except shell.ShellError as ex:
            raise utils.SetupError("Failed to install Homebrew.") from ex

        # fix “zsh compinit: insecure directories” error
        shell.run(f'chmod -R go-w "$({self.brew} --prefix)/share"')
        LOGGER.info("Fixed zsh `compinit` security error.")  # REVIEW: needed?

    def __del__(self) -> None:
        LOGGER.debug("Cleaning up...")
        shell.run(f"{self.brew} cleanup --prune=all", throws=False)
        LOGGER.debug("Homebrew cleanup complete.")
