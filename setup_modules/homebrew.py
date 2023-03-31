"""Setup module containing a `setup` function for setting up Homebrew on a new
machine.
"""

import os
from enum import Enum

from resources import homebrew_packages
from utils.display import Display
from utils.shell import Shell

_display: Display = Display(no_logging=True)
"""The display for printing messages."""
_shell: Shell = Shell()
"""The shell for running commands."""
_silent: bool = False
"""Whether to run the script silently."""


def setup(display=_display, shell=_shell, silent=_silent) -> None:
    """Setup Homebrew on a new machine by installing Homebrew and its packages.

    A `Display` object is used to print messages and log them to a file. A
    non-logging `Display` object is used by default.

    Args:
        display (Display, optional): The display for printing messages.
        shell (Shell, optional): The shell for running commands.
        silent (bool, optional): Whether to run the script silently.
    """
    global _display, _shell, _silent

    # use provided display and shell if any
    _display, _shell, _silent = display, shell, silent
    _display.header("Setting up Homebrew...")

    # Install Homebrew if it is not installed
    _install_brew()

    # add homebrew to path
    cmd = 'eval "$(/opt/homebrew/bin/brew shellenv)"'
    if _shell.run(cmd, _display.debug, _display.error) != 0:
        raise RuntimeError("Failed to add Homebrew to path.")
    _display.verbose("Added Homebrew to path.")

    # fix “zsh compinit: insecure directories” message
    cmd = 'chmod -R go-w "$(brew --prefix)/share"'
    if _shell.run(cmd, _display.debug, _display.error) != 0:
        raise RuntimeError("Failed to fix zsh `compinit` message.")
    _display.verbose("Fixed zsh `compinit` message.")

    # add fonts tap
    cmd = 'brew tap homebrew/cask-fonts'
    if _shell.run_quiet(cmd, _display.debug, "Adding fonts tap") != 0:
        raise RuntimeError("Failed to add fonts tap.")
    _display.verbose("Added fonts tap.")

    # confirm packages if not silent before parsing and installing
    if not _silent:
        _display.info(f"\nPackages file: {homebrew_packages}")
        _display.warning(f"Check packages in the file before continuing.")
        answer = input(f"Do you want to continue setup? (y/n [y]) ")
        if answer or answer.lower()[0] == "n":
            raise KeyboardInterrupt("Packages installation cancelled.")

    # parse Homebrew packages file
    packages = _parse_packages(homebrew_packages)
    _display.verbose("Parsed Homebrew packages file:" + homebrew_packages)

    # install Homebrew packages
    _display.print("Installing Homebrew packages...")
    for package in packages[0]:
        _install_package(package, 'brew', package)
    # install Homebrew casks and fonts
    _display.print("Installing Homebrew casks and fonts...")
    for cask in packages[1]:
        _install_package(cask, 'cask', cask)
    # install MAS apps
    _display.print("Installing App store applications...")
    for app, app_name in packages[2].items():
        _install_package(app, 'mas', app_name)

    _display.success("Homebrew was setup successfully.")


def _install_brew():
    """Install Homebrew on a new machine by running the Homebrew installation
    script.

    Raises:
        KeyboardInterrupt: If the installation is cancelled.
    """
    global _display, _shell

    # check if Homebrew is already installed
    if _shell.run('command -v brew', _display.debug, _display.error) == 0:
        _display.info("Homebrew is already installed.")
        # update Homebrew if it is installed
        _display.verbose("Updating Homebrew...")
        cmd = 'brew update'
        if _shell.run_quiet(cmd, _display.debug, "Updating Homebrew") != 0:
            raise RuntimeError("Failed to update Homebrew.")
        _display.success("Homebrew was updated.")
        return

    # install Homebrew otherwise
    cmd = '/bin/bash -c "$(curl -fsSL https://git.io/JIY6g)"'
    _display.verbose("Installing Homebrew...")
    if _shell.run_quiet(cmd, _display.debug, "Installing Homebrew") != 0:
        raise RuntimeError("Failed to install Homebrew.")
    _display.success("Homebrew was installed.")


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


def _install_package(package: str, type: str, name: str) -> None:
    """Install a package using Homebrew of the given type.

    Args:
        package (str): The name of the package to install.
        type (str): The type of the package to install (brew, cask, or mas).
        name (str): The name of the package to display to the user.
    """
    global _display, _shell
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
    _display.verbose(f"    Installing {package}...")
    if _shell.run_quiet(cmd, _display.debug, f"    Installing {name}") != 0:
        _display.error(f"    Failed to install {name}.")
        return
    _display.success(f"    {name} was installed.")


if __name__ == "__main__":
    setup()
