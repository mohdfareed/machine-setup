#!/usr/bin/env python3
"""Bootstrap a new macOS machine. This will clone machine configuration and
execute the setup script.

Requirements: Xcode Commandline Tools.

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
import urllib.request

REPO = "https://github.com/mohdfareed/machine.git"
"""URL of the repository to clone."""
SOURCE_URL = "https://raw.githubusercontent.com/mohdfareed/machine/main"
"""URL of the shell environment file."""
MACHINE_VAR = "machine"
"""Environment variable to resolve machine config path."""

# paths at machine repository
ZSHENV = os.path.join("config", "zshenv")
REQUIREMENTS = "requirements.txt"
SETUP_SCRIPT = "setup.sh"
VENV = ".venv"


def main(machine: str, overwrite=False, setup_args=None) -> None:
    """Bootstrap the machine setup process."""

    # fetch machine shell environment file
    shell_env = os.path.join(SOURCE_URL, machine, ZSHENV)
    with urllib.request.urlopen(shell_env) as response:
        env_file = response.read().decode()

    # resolve machine path
    cmd = [f"eval '{env_file}' > /dev/null; echo ${MACHINE_VAR}"]
    machine_path = run(cmd[0], silent=True, text=True)
    machine_path = os.path.realpath(machine_path)

    # clone machine, overwrite if prompted
    print(f"Cloning machine into: {machine_path}")
    if overwrite and os.path.exists(machine_path):
        print("Removing existing machine...")
        shutil.rmtree(machine_path, ignore_errors=True)
    if not os.path.exists(machine_path):  # clone machine otherwise
        run(["git", "clone", "-q", REPO, machine_path], silent=True)

    # create virtual environment
    print("Creating virtual environment...")
    venv_options = "--clear --upgrade-deps --prompt machine"
    machine_venv_path = os.path.join(machine_path, VENV)
    run(f"python3 -m venv {machine_venv_path} {venv_options}", silent=True)

    # install dependencies
    python = os.path.join(machine_venv_path, "bin", "python")
    req_file = os.path.join(machine_path, REQUIREMENTS)
    cmd = [python, "-m", "pip", "install", "-r", req_file, "--upgrade"]
    run(cmd, silent=True)  # install dependencies

    # execute machine setup script
    script = os.path.join(machine_path, SETUP_SCRIPT)
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
        choices=["macos", "rpi"],
        help="specify the type of machine to setup",
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
    force = args.force
    additional_args = args.args

    try:
        main(machine_name, force, additional_args)
    except Exception as e:  # pylint: disable=broad-except
        print(f"\033[31;1m{'Error:'}\033[0m {e}")
        print(f"\033[31;1m{'Failed to bootstrap machine'}\033[0m")
        sys.exit(1)
