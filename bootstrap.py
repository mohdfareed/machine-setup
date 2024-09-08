#!/usr/bin/env python3
"""Bootstrap a new machine. This will clone the machine's configuration and
execute the setup script.

Requirements:
    - Python 3.7+
    - git must be installed
    - machine module with a setup script
    - requirements.txt file with dependencies

External effects:
    - Clones machine into the specified path
    - Creates a virtual environment
    - Installs dependencies
    - Executes the setup script
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys

REPOSITORY = "https://github.com/mohdfareed/machine.git"
"""Machine configuration repository."""
VIRTUAL_ENV = ".venv"
"""Virtual environment directory name."""
REQUIREMENTS = "requirements.txt"
"""Requirements file name."""
MODULE = "machines.{}.setup"
"""Machine setup module name."""

DEFAULT_MACHINE = "codespaces" if os.environ.get("CODESPACES") else None
"""Default machine name."""
DEFAULT_MACHINE_PATH = os.environ.get("MACHINE") or os.path.join(
    os.path.expanduser("~"), ".machine"
)  # default to $MACHINE or ~/.machine
"""Default path to clone the machine repository."""


def main(
    machine=DEFAULT_MACHINE,
    path=DEFAULT_MACHINE_PATH,
    overwrite=False,
    setup_args=None,
):
    """Bootstrap the machine setup process."""
    path = os.path.realpath(path)
    if not machine:
        raise ValueError("Machine name not provided.")

    # set up environment
    clone_machine(path, overwrite)
    module = MODULE.format(machine)
    module_path = os.path.join(path, *module.split(".")) + ".py"
    if not os.path.exists(module_path):
        raise FileNotFoundError(f"Machine '{machine}' not found.")

    # bootstrap machine
    python = create_virtual_env(path, machine)
    install_dependencies(python, path)
    setup_machine(python, module, path, setup_args)


def clone_machine(path: str, clean: bool):
    """Clone the machine repository into the specified path."""
    if clean and os.path.exists(path):  # remove existing
        shutil.rmtree(path, ignore_errors=True)
    if not os.path.exists(path):  # clone if not exists
        subprocess.run(["git", "clone", "-q", REPOSITORY, path], check=True)

    else:  # pull latest changes if exists
        if (  # warn user if there are uncommitted changes
            subprocess.run(
                ["git", "diff", "--quiet"], cwd=path, check=False
            ).returncode
            != 0
        ):
            print(f"\033[33m{'WARNING'}\033[0m  Uncommitted changes found.")
            return
        subprocess.run(["git", "pull", "-q"], cwd=path, check=True)


def create_virtual_env(path: str, prompt: str) -> str:
    """Create a virtual environment in the specified path.
    Return the python executable path."""
    venv = os.path.join(path, VIRTUAL_ENV)
    opts = ["--clear", "--prompt", prompt, "--upgrade-deps"]
    subprocess.run(["python3", "-m", "venv", *opts, venv], check=True)
    bin_path = "bin" if platform.system() != (_ := "Windows") else "Scripts"
    return os.path.join(venv, bin_path, "python")


def install_dependencies(python: str, path: str):
    """Install and/or upgrade dependencies from the requirements file."""
    req_file = os.path.join(path, REQUIREMENTS)
    cmd = [python, "-m", "pip", "install", "-r", req_file, "--upgrade"]
    subprocess.run(cmd, capture_output=True, check=True)


def setup_machine(python: str, machine: str, path: str, setup_args=None):
    """Bootstrap the machine setup process."""
    setup = [python, "-m", machine, *(setup_args or [])]
    subprocess.run(setup, cwd=path, check=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Bootstrap a new machine.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="overwrite machine if it exists",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="the path to the machine repo",
        default=DEFAULT_MACHINE_PATH,
    )
    parser.add_argument(
        "machine",
        type=str,
        help="the machine to bootstrap",
        nargs="?",
        default=DEFAULT_MACHINE,
    )
    parser.add_argument(
        "args", nargs=argparse.REMAINDER, help="additional setup arguments"
    )

    # parse arguments
    args = parser.parse_args()
    force = args.force
    machine_path = args.path
    machine_name = args.machine
    additional_args = args.args

    try:
        main(machine_name, machine_path, force, additional_args)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:  # pylint: disable=broad-except
        print(f"\033[31m{'ERROR'}\033[0m    {e}")
        print(f"\033[31;1m{'Failed to bootstrap machine.'}\033[0m")
        sys.exit(1)
