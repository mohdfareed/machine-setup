"""Setup module containing a `setup` function for setting up Homebrew on a new
machine.
"""

from config import homebrew_packages
from utils import shell
from utils.logger import Display

DISPLAY: Display = Display(no_logging=True)
"""The default display for printing messages."""


def setup(display=DISPLAY) -> None:
    """Setup Homebrew on a new machine by installing Homebrew and its packages.

    A `Display` object is used to print messages and log them to a file. A
    non-logging `Display` object is used by default.

    Args:
        display (Display, optional): The display for printing messages.
    """
    display.header("Setting up Homebrew...")

    # Install Homebrew if it is not installed
    _install_brew(display)

    # add homebrew to path
    cmd = 'eval "$(/opt/homebrew/bin/brew shellenv)"'
    if shell.run(cmd, display.debug, display.error) != 0:
        raise RuntimeError("Failed to add Homebrew to path.")
    display.verbose("Added Homebrew to path.")

    # fix “zsh compinit: insecure directories” error
    cmd = 'chmod -R go-w "$(brew --prefix)/share"'
    if shell.run(cmd, display.debug, display.error) != 0:
        raise RuntimeError("Failed to fix zsh `compinit` message.")
    display.verbose("Fixed zsh `compinit` error.")  # TODO: check if needed

    # add fonts tap
    cmd = "brew tap homebrew/cask-fonts"
    if shell.run_quiet(cmd, display.debug, "Adding fonts tap") != 0:
        raise RuntimeError("Failed to add fonts tap.")
    display.verbose("Added fonts tap.")

    # parse Homebrew packages file
    packages = _parse_packages(homebrew_packages)
    display.verbose("Parsed Homebrew packages file:" + homebrew_packages)

    # install Homebrew packages
    display.print("Installing Homebrew packages...")
    for package in packages[0]:
        install_package(display, package)
    # install Homebrew casks and fonts
    display.print("Installing Homebrew casks and fonts...")
    for cask in packages[1]:
        install_package(display, cask, cask=True)

    display.success("Homebrew was setup successfully.")


def install_package(display: Display, package: str, cask: bool = False):
    """Install a package or cask using Homebrew.

    Args:
        display (Display): The display for printing messages.
        package (str): The name of the package to install.
        cask (bool): Whether the package is a cask.
    """
    # set command based on type
    if cask:
        cmd = f"brew install --cask {package}"
    else:
        cmd = f"brew install {package}"

    # install package
    display.debug(f"Installing {package}...")
    if shell.run_quiet(cmd, display.debug, f"Installing {package}") != 0:
        display.error(f"Failed to install {package}.")
        return
    display.success(f"{package} was installed.")


def _install_brew(display):
    """Install Homebrew on a new machine by running the Homebrew installation
    script.

    Raises:
        KeyboardInterrupt: If the installation is cancelled.
    """
    # check if Homebrew is already installed
    if shell.run("command -v brew", display.debug, display.error) == 0:
        display.info("Homebrew is already installed.")
        # update Homebrew if it is installed
        display.verbose("Updating Homebrew...")
        cmd = "brew update"
        if shell.run_quiet(cmd, display.debug, "Updating Homebrew") != 0:
            raise RuntimeError("Failed to update Homebrew.")
        display.success("Homebrew was updated.")
        return

    # install Homebrew otherwise
    cmd = '/bin/bash -c "$(curl -fsSL https://git.io/JIY6g)"'
    display.verbose("Installing Homebrew...")
    if shell.run_quiet(cmd, display.debug, "Installing Homebrew") != 0:
        raise RuntimeError("Failed to install Homebrew.")
    # source Homebrew
    cmd = 'eval "$(/opt/homebrew/bin/brew shellenv)"'
    if shell.run(cmd, display.debug, display.error) != 0:
        raise RuntimeError("An error occurred while installing Homebrew.")
    display.success("Homebrew was installed.")


def _parse_packages(file_path: str) -> tuple[list, list]:
    """Parse a file containing Homebrew packages. The file is expected to have
    packages separated by newlines. Packages can either be brew packages or
    casks. Casks are expected to be prefixed with `cask`.

    Args:
        file_path (str): The path to the file containing Homebrew packages.

    Returns:
        tuple[list, list]: the packages and casks
    """
    import os

    packages = []
    casks = []

    # check if file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Packages file not found at: {file_path}")

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            line = line.split("#")[0].strip()  # remove comments
            # parse brew packages
            if line.startswith("brew"):
                packages.append(line.split(" ")[1].strip('"'))
            # parse cask packages
            elif line.startswith("cask "):
                casks.append(line.split(" ")[1].strip('"'))

    return packages, casks


if __name__ == "__main__":
    setup()
