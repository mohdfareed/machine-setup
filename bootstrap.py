#!/usr/bin/env python3
"""Bootstrap a new machine. This will clone the machine's configuration and
execute the setup script.

Requirements:
    - Configured `[machine]` module in the repository
    - `[machine]/setup.py` setup script
    - `[machine]/config/zshenv` shell environment file
    - `$MACHINE` environment variable to resolve machine path

External effects:
    - Clones machine into `$MACHINE`
    - Creates a virtual environment at `$MACHINE`
    - Executes `setup.sh`
"""

import argparse
import os
import shutil
import subprocess
import sys

REPO = "https://github.com/mohdfareed/machine.git"
"""URL of the repository to clone."""
SOURCE_URL = "https://raw.githubusercontent.com/mohdfareed/machine/main"
"""URL of the shell environment file."""
MACHINE_VAR = "MACHINE"
"""Environment variable to resolve machine config path."""

# paths at machine repository
ZSHENV = os.path.join("config", "zshenv")
REQUIREMENTS = "requirements.txt"
SETUP_SCRIPT = "setup.sh"
VENV = ".venv"


def main(machine: str, path: str, overwrite=False, setup_args=None) -> None:
    """Bootstrap the machine setup process."""

    # clone machine, overwrite if prompted
    print(f"Cloning machine into: {path}")
    if overwrite and os.path.exists(path):
        print("Removing existing machine...")
        shutil.rmtree(path, ignore_errors=True)
    if not os.path.exists(path):  # clone machine otherwise
        run(["git", "clone", "-q", REPO, path], silent=True)

    # create virtual environment
    print("Creating virtual environment...")
    venv_options = "--clear --upgrade-deps --prompt machine"
    machine_venv_path = os.path.join(path, VENV)
    run(f"python3 -m venv {machine_venv_path} {venv_options}", silent=True)

    # install dependencies
    python = os.path.join(machine_venv_path, "bin", "python")
    req_file = os.path.join(path, REQUIREMENTS)
    cmd = [python, "-m", "pip", "install", "-r", req_file, "--upgrade"]
    run(cmd, silent=True)  # install dependencies

    # execute machine setup script
    script = os.path.join(path, SETUP_SCRIPT)
    run(f"{script} {machine} {' '.join(setup_args or [])}", safe=False)


def run(cmd, silent=False, safe=False, text=False):
    """Run a shell command."""
    options: dict = dict(capture_output=silent, text=text)
    result = subprocess.run(
        cmd, shell=isinstance(cmd, str), check=not safe, **options
    )
    return result.stdout.strip() if text else result.returncode


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap machine setup.")
    parser.add_argument(
        "machine",
        type=str,
        choices=["macos", "rpi", "codespaces"],
        help="the machine to setup",
    )
    parser.add_argument(
        "path",
        type=str,
        help="the path to the machine repo",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="overwrite machine if it exists",
    )
    parser.add_argument("args", nargs=argparse.REMAINDER)

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
        print(f"\033[31;1m{'Failed to bootstrap machine'}\033[0m")
        sys.exit(1)
