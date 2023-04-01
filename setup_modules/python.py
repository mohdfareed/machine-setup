"""Setup module containing a `setup` function for setting up Python on a new
machine.
"""

from resources import python_packages
from utils import abs_path, create_file, shell, symlink
from utils.display import Display

from .homebrew import install_package

DISPLAY: Display = Display(no_logging=True)
"""The default display for printing messages."""


def setup(display=DISPLAY) -> None:
    """Setup Python on a new machine by installing it through Homebrew and
    installing its packages.

    A `Display` object is used to print messages and log them to a file. A
    non-logging `Display` object is used by default.

    Args:
        display (Display, optional): The display for printing messages.
    """
    display.header("Setting up Python...")

    # check if homebrew is installed and install python
    if shell.run('command -v brew', display.verbose, display.error) != 0:
        raise RuntimeError("Could not find Homebrew.")
    display.debug("Homebrew was found.")
    install_package(display, "python")

    # parse packages file
    packages = _parse_packages(python_packages)
    display.debug("Packages file was parsed.")

    # TODO: install packages
    for package in packages:
        display.print(f"Installing {package[0]}...")
        if package[1]:
            display.print(f"    Version:{package[1]}")

    display.success("Python was setup successfully.")


def _parse_packages(file_path: str) -> list[tuple]:
    """Parse a file containing Python packages. The file is expected to have
    packages and their versions separated by new lines.

    Args:
        file_path (str): The path to the file containing Homebrew packages.

    Returns:
        list[tuple]: the packages names and versions as a list of tuples.
    """
    import os
    packages = []

    # check if file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Packages file not found at: {file_path}")

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # parse package if not a comment
            if line and not line.startswith('#'):
                line = line.split('#')[0].strip()  # remove comments
                # parse package name and version
                name = line.split('==')[0].strip()
                version = line.split('==')[1].strip() if '==' in line else None
                packages.append((name, version))

    return packages


if __name__ == "__main__":
    setup()
