"""Setup module containing a `setup` function for setting up Homebrew on a new
machine.
"""

import os

from resources import homebrew_packages
from utils import shell
from utils.display import Display

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
    if shell.run(cmd, display.verbose, display.error) != 0:
        raise RuntimeError("Failed to add Homebrew to path.")
    display.debug("Added Homebrew to path.")

    # fix “zsh compinit: insecure directories” error
    cmd = 'chmod -R go-w "$(brew --prefix)/share"'
    if shell.run(cmd, display.verbose, display.error) != 0:
        raise RuntimeError("Failed to fix zsh `compinit` message.")
    display.debug("Fixed zsh `compinit` error.")  # TODO: check if needed

    # add fonts tap
    cmd = 'brew tap homebrew/cask-fonts'
    if shell.run_quiet(cmd, display.verbose, "Adding fonts tap") != 0:
        raise RuntimeError("Failed to add fonts tap.")
    display.debug("Added fonts tap.")

    # confirm packages before parsing and installing
    display.info(f"\nPackages file: {homebrew_packages}")
    input(f"Press any key to continue...\n")

    # parse Homebrew packages file
    packages = _parse_packages(homebrew_packages)
    display.debug("Parsed Homebrew packages file:" + homebrew_packages)

    # install Homebrew packages
    display.print("Installing Homebrew packages...")
    for package in packages[0]:
        _install_package(display, package, 'brew', package)
    # install Homebrew casks and fonts
    display.print("Installing Homebrew casks and fonts...")
    for cask in packages[1]:
        _install_package(display, cask, 'cask', cask)
    # install MAS apps
    display.print("Installing App store applications...")
    for app, app_name in packages[2].items():
        _install_package(display, app, 'mas', app_name)

    display.success("Homebrew was setup successfully.")


def _install_brew(display):
    """Install Homebrew on a new machine by running the Homebrew installation
    script.

    Raises:
        KeyboardInterrupt: If the installation is cancelled.
    """
    # check if Homebrew is already installed
    if shell.run('command -v brew', display.verbose, display.error) == 0:
        display.info("Homebrew is already installed.")
        # update Homebrew if it is installed
        display.debug("Updating Homebrew...")
        cmd = 'brew update'
        if shell.run_quiet(cmd, display.verbose, "Updating Homebrew") != 0:
            raise RuntimeError("Failed to update Homebrew.")
        display.success("Homebrew was updated.")
        return

    # install Homebrew otherwise
    cmd = '/bin/bash -c "$(curl -fsSL https://git.io/JIY6g)"'
    display.verbose("Installing Homebrew...")
    if shell.run_quiet(cmd, display.verbose, "Installing Homebrew") != 0:
        raise RuntimeError("Failed to install Homebrew.")
    display.success("Homebrew was installed.")


def _parse_packages(file_path: str) -> tuple[list, list, dict]:
    """Parse a file containing Homebrew packages. The file is expected to have
    packages separated by newlines. Packages can be of three types: brew, cask,
    and mas. The mas is a dictionary of ids as keys and names as values.

    Args:
        file_path (str): The path to the file containing Homebrew packages.

    Returns:
        tuple[list, list, dict]: the packages in the order brew, cask, and mas.
    """
    packages = []
    casks = []
    mas = {}

    # check if file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Packages file not found at: {file_path}")

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # parse brew packages
            if line.startswith('brew '):
                packages.append(line.split('"')[1])
            # parse cask packages
            elif line.startswith('cask '):
                casks.append(line.split('"')[1])
            # parse mas package IDs and their names
            elif line.startswith('mas '):
                id = line.split('"')[2].split(':')[1].strip()
                mas[id] = line.split('"')[1]

    return packages, casks, mas


def _install_package(display, package, type, name) -> None:
    """Install a package using Homebrew of the given type.

    Args:
        package (str): The name of the package to install.
        type (str): The type of the package to install (brew, cask, or mas).
        name (str): The name of the package to display to the user.
    """
    if type not in ['brew', 'cask', 'mas']:
        raise ValueError(f"Invalid package type: {type}")

    # set command based on type
    if type == 'brew':
        cmd = f"brew install {package}"
    elif type == 'cask':
        cmd = f"brew install --cask {package}"
    else:
        cmd = f"mas install {package}"

    # install package
    display.debug(f"    Installing {name}...")
    if shell.run_quiet(cmd, display.verbose, f"    Installing {name}") != 0:
        display.error(f"    Failed to install {name}.")
        return
    display.success(f"    {name} was installed.")


if __name__ == "__main__":
    setup()
