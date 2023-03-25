"""Setup module containing a `setup` function for setting up Homebrew on a new
machine.
"""

import os
from utils.display import Display
from utils.shell import Shell
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
    display.verbose("Adding Homebrew to path...")
    command = 'eval "$(/opt/homebrew/bin/brew shellenv)"'
    returncode = shell.run(command, display.verbose, display.error)
    if returncode != 0:
        display.error("Failed to add Homebrew to path.")
        return
    display.verbose("Added Homebrew to path.")

    # fix “zsh compinit: insecure directories” message
    display.verbose("Fixing zsh `compinit` message...")
    command = 'chmod -R go-w "$(brew --prefix)/share"'
    returncode = shell.run(command, display.verbose, display.error)
    if returncode != 0:
        display.error("Failed to fix zsh `compinit` message.")
        return
    display.verbose("Fixed zsh `compinit` message.")

    # add fonts tap
    display.verbose("Adding fonts tap...")
    command = 'brew tap homebrew/cask-fonts'
    returncode = shell.run_quiet(command, display.verbose, "Adding fonts tap")
    if returncode != 0:
        display.error("Failed to add fonts tap.")
        return
    display.verbose("Added fonts tap.")

    # read Homebrew packages
    display.verbose("Parsing Homebrew packages...")
    try:
        packages, casks, fonts, mas = _parse_packages(homebrew_packages)
    except Exception as e:
        display.error("Failed to parse Homebrew packages file.")
        display.debug(str(e))
        return

    # output Homebrew packages as debug logs
    display.debug("Packages found:\n    " + "\n    ".join(packages))
    display.debug("Casks found:\n    " + "\n    ".join(casks))
    display.debug("Fonts found:\n    " + "\n    ".join(fonts))
    display.debug("MAS apps found:\n    " + "\n    ".join(mas[0]))

    # install Homebrew packages
    display.print("Installing Homebrew packages:")
    for package in packages:
        display.verbose(f"Installing {package}...")
        _prompt_package(package, 'package', display, shell, silent)
    # install Homebrew casks and fonts
    display.print("Installing Homebrew casks and fonts:")
    for cask in casks + fonts:  # fonts are installed as casks
        display.verbose(f"Installing {cask}...")
        _prompt_package(cask, 'cask', display, shell, silent)
    # install MAS apps
    display.print("Installing App store applications:")
    for app in mas[1]:
        display.verbose(f"Installing {app} ({mas[0][mas[1].index(app)]})...")
        _prompt_package(app, 'mas', display, shell, silent,
                        name=mas[0][mas[1].index(app)])

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


def _parse_packages(file_path: str) -> tuple[list[str], list[str], list[str],
                                             list[list[str]]]:
    """Parse a file containing Homebrew packages. The file is expected to have
    packages separated by newlines. Packages can be of four types: brew, cask,
    font, and mas. The mas list contains two lists: the first contains the
    package IDs and the second contains the package names.

    Args:
        file_path (str): The path to the file containing Homebrew packages.

    Returns:
        tuple[list[str], list[str], list[str], list[list[str]]]]: the packages
        in the order brew, cask, font, and mas.
    """
    packages = []
    casks = []
    fonts = []
    mas = [[], []]  # [id, name]

    # check if file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Homebrew file not found: {file_path}")

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if line.startswith('brew '):
                packages.append(line.split('"')[1])

            elif line.startswith('cask "font-'):
                fonts.append(line.split('"')[1])

            elif line.startswith('cask '):
                casks.append(line.split('"')[1])

            elif line.startswith('mas '):
                mas[1].append(line.split('"')[2].split(':')[1].strip())
                mas[0].append(line.split('"')[1])

    return packages, casks, fonts, mas


def _prompt_package(package: str, type: str, display: Display, shell: Shell,
                    silent: bool, name: str | None = None) -> None:
    """Prompt the user to install a Homebrew package. It will install the
    package if the user enters "y" or "yes".

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
    # prompt user to install package if not silent
    if not silent:
        answer = input(f"Do you want to install {name}? (y/n [n]) ")
        if not answer or answer.lower()[0] != "y":
            display.verbose(f"Skipped installing {name}.")
            return

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
