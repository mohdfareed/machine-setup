"""Setup module containing a `setup` function for setting up Homebrew on a new
machine.
"""

import os
from utils.display import Display
from utils.shell import Shell
from utils.colors import LINE_UP, LINE_CLEAR
from typing import Callable
from resources import homebrew_packages


def setup(display: Display = Display(no_logging=True), shell: Shell = Shell(),
          silent: bool = False) -> None:
    """Setup Homebrew on a new machine by installing Homebrew and its packages.

    A `Display` object is used to print messages and log them to a file. A
    non-logging `Display` object is used by default.

    Args:
        display (Display, optional): The display for printing messages.
    """
    display.header("Setting up Homebrew...")

    # Install Homebrew if it is not installed
    display.verbose("Installing Homebrew...")
    if not _install_brew(display, shell):
        return

    # add homebrew to path
    command = 'eval "$(/opt/homebrew/bin/brew shellenv)"'
    returncode = shell.run(command, display.verbose, display.error)
    if returncode != 0:
        display.error("Failed to add Homebrew to path.")
        return
    display.verbose("Added Homebrew to path.")

    # fix “zsh compinit: insecure directories” message
    command = 'chmod -R go-w "$(brew --prefix)/share"'
    returncode = shell.run(command, display.verbose, display.error)
    if returncode != 0:
        display.error("Failed to fix zsh `compinit` message.")
        return
    display.verbose("Fixed zsh `compinit` message.")

    # add fonts tap
    command = 'brew tap homebrew/cask-fonts'
    returncode = shell.run_quiet(command, display.verbose, "Adding fonts tap")
    if returncode != 0:
        display.error("Failed to add fonts tap.")
        return
    display.verbose("Added fonts tap.")

    # parse Homebrew packages file
    try:
        packages = _parse_packages(homebrew_packages)
    except Exception as e:
        display.error("Failed to parse Homebrew packages file.")
        display.debug(str(e))
        return
    display.verbose("Parsed Homebrew packages file.")

    # prompt for Homebrew packages to install if not in silent mode
    if not silent:
        packages = _select_packages(packages, display.print)
        display.verbose("Homebrew packages selected.")

    # install Homebrew packages
    display.print("Installing Homebrew packages...")
    for package in packages[0]:
        display.verbose(f"Installing {package}...")
        _install_package(package, 'package', display, shell)

    # install Homebrew casks and fonts
    display.print("Installing Homebrew casks and fonts...")
    for cask in packages[1]:
        display.verbose(f"Installing {cask}...")
        _install_package(cask, 'cask', display, shell)

    # install MAS apps
    display.print("Installing App store applications...")
    for app in packages[2].keys():
        display.verbose(f"Installing {packages[2][app]} ({app})...")
        _install_package(app, 'mas', display, shell, packages[2][app])

    display.success("")
    display.success("Homebrew was setup successfully.")


def _install_brew(display: Display, shell: Shell) -> bool:
    """Install Homebrew on a new machine by running the Homebrew installation
    script.

    Args:
        display (Display): The display for printing messages.
        shell (Shell): The shell for running commands.

    Returns:
        bool: True if Homebrew was installed successfully, False otherwise.
    """
    # check if Homebrew is already installed
    if shell.run('command -v brew', display.debug, display.error) == 0:
        display.info("Homebrew is already installed.")
        # update Homebrew if it is installed
        returncode = shell.run_quiet('brew update', display.verbose,
                                     loading_string="Updating Homebrew")
        # check if Homebrew was updated successfully
        if returncode == 0:
            display.success("Homebrew was updated.")
            return True
        display.error("Failed to update Homebrew.")
        return False

    # install Homebrew otherwise
    command = '/bin/bash -c "$(curl -fsSL https://git.io/JIY6g)"'
    returncode = shell.run_quiet(command, display.verbose,
                                 loading_string="Installing Homebrew")
    # check if Homebrew was installed successfully
    if returncode == 0:
        display.success("Homebrew was installed.")
        return True
    display.error("Failed to install Homebrew.")
    return False


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
        raise FileNotFoundError(f"Homebrew file not found: {file_path}")

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if line.startswith('brew '):
                packages.append(line.split('"')[1])

            elif line.startswith('cask '):
                casks.append(line.split('"')[1])

            elif line.startswith('mas '):
                id = line.split('"')[2].split(':')[1].strip()
                name = line.split('"')[1]
                mas[id] = name

    return packages, casks, mas


def _select_packages(packages: tuple[list, list, dict],
                     printer: Callable) -> tuple[list, list, dict]:
    """Prompt the user to choose which packages to install. It takes a tuple of
    packages in the order brew, cask, font, and mas. It returns a tuple of the
    same format with the packages that the user chose.

    Args:
        packages (tuple): The list of packages from which to choose.
        printer (Display): The display for printing prompts.
    """

    while True:
        chosen_packages = _prompt_package(packages[0])
        chosen_casks = _prompt_package(packages[1])
        chosen_mas = _prompt_package(list(packages[2].values()))
        chosen_mas = {k: v for k, v in packages[2].items() if v in chosen_mas}

        # print chosen packages

        printer("Selected packages:")
        printer("\n".join(chosen_packages))

        printer("Selected casks and fonts:")
        printer("\n".join(chosen_casks))

        printer("Selected App Store apps:")
        printer("\n".join(list(chosen_mas.values())))

        # prompt user to confirm packages
        answer = input("Do you want to continue? (y/n [n]): ")
        if answer and answer.lower()[0] == "y":
            return chosen_packages, chosen_casks, chosen_mas


def _prompt_package(packages: list[str]) -> list[str]:
    """Prompt the user to choose which packages to install from a list of
    packages.

    Args:
        packages (list[str]): The list of packages from which to choose.
    """
    selected_packages = []
    for package in packages:
        answer = input(f"Do you want to install '{package}'? (y/n [n]): ")
        print(LINE_UP + LINE_CLEAR + LINE_UP)
        if answer.lower() == "y":
            selected_packages.append(package)
    return selected_packages


def _install_package(package: str, type: str, display: Display, shell: Shell,
                     name: str | None = None) -> None:
    """Install a package using Homebrew of the given type.

    Args:
        package (str): The name of the package to install.
        type (str): The type of the package (e.g. "package", "cask", or "mas").
        display (Display): The display for printing messages.
        shell (Shell): The shell for running installation commands.
        silent (bool): Whether to install the package silently without prompts.
        name (str): The name of the package to display to the user. If None,
        the package name will be used.
    """
    # set name to package if name is None
    name = name if name else package

    # set command based on type
    if type == "mas":
        command = f"mas install {package}"
    elif type == "cask":
        command = f"brew install --cask {package}"
    else:
        command = f"brew install {package}"

    # install package or cask
    returncode = shell.run_quiet(command, display.verbose,
                                 loading_string=f"Installing {name}")
    # check if package was installed successfully
    if returncode == 0:
        display.success(f"    {name} was installed.")
    else:
        display.error(f"    Failed to install {name}.")


if __name__ == "__main__":
    setup()
