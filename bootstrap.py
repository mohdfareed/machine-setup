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

REPO = "https://github.com/mohdfareed/machine.git"
"""URL of the repository to clone."""
_WIN_PLATFORM = "Windows"

default_machine_path = os.environ.get("MACHINE") or os.path.join(
    os.path.expanduser("~"), ".machine"
)  # default to $MACHINE or ~/.machine
"""Default path to clone the machine repository."""


def main(machine: str, path: str, overwrite=False, setup_args=None) -> None:
    """Bootstrap the machine setup process."""
    # validate arguments
    path, req_file = validate_machine(machine, path)

    # clone machine, overwrite if necessary
    if overwrite and os.path.exists(path):
        print("Removing existing machine...")
        shutil.rmtree(path, ignore_errors=True)
    elif not os.path.exists(path):
        print(f"Cloning machine into: {path}")
        clone_machine(REPO, path)

    # create virtual environment
    print("Creating virtual environment...")
    venv = os.path.join(path, ".venv")
    python = create_virtual_env(venv, machine)
    print("Installing dependencies...")
    install_dependencies(python, req_file)

    # execute machine setup script
    print(f"Setting up machine: {machine}")
    setup_machine(python, machine, path, setup_args)


def clone_machine(repo: str, path: str) -> None:
    """Clone the machine repository into the specified path."""
    subprocess.run(["git", "clone", "-q", repo, path], check=True)


def create_virtual_env(venv: str, prompt: str) -> str:
    """Create a virtual environment in the specified path. Return the python
    executable path."""
    opts = ["--clear", "--prompt", prompt, "--upgrade-deps"]
    subprocess.run(["python3", "-m", "venv", *opts, venv], check=True)
    python = os.path.join(
        venv,
        "bin" if platform.system() != _WIN_PLATFORM else "Scripts",
        "python",
    )

    if not os.path.exists(python):
        raise FileNotFoundError("Python executable not found.")
    return python


def install_dependencies(python: str, req_file: str) -> None:
    """Install and/or upgrade dependencies from the requirements file."""
    cmd = [python, "-m", "pip", "install", "-r", req_file, "--upgrade"]
    subprocess.run(cmd, capture_output=True, check=True)


def setup_machine(
    python: str, machine: str, path: str, setup_args=None
) -> None:
    """Bootstrap the machine setup process."""
    setup = [python, "-m", f"machines.{machine}.setup", *(setup_args or [])]
    os.chdir(path)
    subprocess.run(setup, check=False)


def validate_machine(machine: str, path: str) -> tuple[str, str]:
    """Validate the machine requirements. Returns machine path."""
    path = path or default_machine_path
    path = os.path.abspath(os.path.realpath(path))

    # check if setting up a github codespace
    if not machine and os.environ.get("CODESPACES"):
        machine = "codespaces"

    module_path = os.path.join(path, "machines", machine, "setup.py")
    module_init = os.path.join(path, "machines", machine, "__init__.py")
    if (
        not machine
        or not os.path.exists(module_path)
        or not os.path.exists(module_init)
    ):
        raise ValueError(f"Machine '{machine}' setup module not found.")

    req_file = os.path.join(path, "requirements.txt")
    if not os.path.exists(req_file):
        raise FileNotFoundError("Requirements file not found.")
    return path, req_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Bootstrap a new machine.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "path",
        type=str,
        help="the path to the machine repo",
        nargs="?",  # Make the argument optional
        default=default_machine_path,
    )
    parser.add_argument("machine", type=str, help="the machine to bootstrap")
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="overwrite machine if it exists",
    )
    parser.add_argument(
        "args", nargs=argparse.REMAINDER, help="additional setup arguments"
    )

    # parse arguments
    args = parser.parse_args()
    machine_name = args.machine
    machine_path = args.path
    force = args.force
    additional_args = args.args

    try:
        main(machine_name, machine_path, force, additional_args)
    except Exception as e:  # pylint: disable=broad-except
        print(f"\033[31;1m{'Error:'}\033[0m {e}")
        print(f"\033[31;1m{'Failed to bootstrap machine.'}\033[0m")
        sys.exit(1)
