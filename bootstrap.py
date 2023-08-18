#!/usr/bin/env python3
"""Bootstrap a new machine. This will install Xcode Commandline Tools, accept
the Xcode license, clone machine, and execute the setup script.

Requirements: Xcode Commandline Tools and `machine.sh` in config directory.
The file must have the environment variable `MACHINE`, which is the path to the
machine repo.

Usage: ./bootstrap.py config_path [-c] [-l] [-d]
 - config_path: path to local config files, which contains:
   - `machine.sh`: machine-specific environment, includes `MACHINE` variable
 - -c | --clean: clean setup environment, overwriting repo and virtual env
 - *: extra arguments are passed to `setup.py`

External effects:
  - Accepts Xcode license
  - Clones machine into `MACHINE`
  - Creates a virtual environment at `MACHINE`
  - Executes `setup.sh` in machine
"""

import argparse
import os
import shutil
import subprocess
from typing import Optional

REPOSITORY = "https://github.com/mohdfareed/machine.git"
"""Repository to clone."""
SCRIPT = "setup.py"
"""Machine setup script filename."""
REQUIREMENTS = "requirements.txt"
"""Virtual environment requirements filename."""
VENV_PATH = ".venv"
"""Path to the virtual environment."""
ENV = "https://raw.githubusercontent.com/mohdfareed/machine/main/config/zshenv"
"""Path to the environment file."""


def main(config_path: Optional[str], overwrite=False, *args):
    """Clone and set up machine."""

    resolve_xcode()  # accept xcode license
    machine_path = load_env()  # resolve machine path
    clone_machine(machine_path, overwrite)  # clone repository
    python = setup_env(machine_path)  # setup virtual environment
    setup(python, machine_path, config_path, *args)  # setup machine


def load_env() -> str:
    _exec(["curl", "-fsSL", ENV, "-o", "temp.sh"], silent=True)
    path = _exec("source temp.sh && echo $MACHINE", silent=True, text=True)
    _exec("rm temp.sh", silent=True)
    return os.path.realpath(path)


def resolve_xcode():
    try:  # accept xcode license
        prompt = "Authenticate to accept Xcode license agreement: "
        _exec(["sudo", "--prompt", prompt, "xcodebuild", "-license", "accept"])
    except subprocess.CalledProcessError:
        _print_error("Failed to accept Xcode license")
        _exec("xcode-select --install", silent=True)  # prompt to install
        exit(1)


def clone_machine(path: str, overwrite=False):
    # overwrite machine if prompted
    if overwrite and os.path.exists(path):
        _print_info("Overwriting machine...")
        shutil.rmtree(path, ignore_errors=True)

    if not os.path.exists(path):  # clone machine
        _print_info(f"Cloning machine into '{path}'...")
        _exec(["git", "clone", "-q", REPOSITORY, path], silent=True)


def setup_env(machine_path: str) -> str:
    req_file = os.path.join(machine_path, REQUIREMENTS)
    machine_venv_path = os.path.join(machine_path, VENV_PATH)
    python = os.path.join(machine_venv_path, "bin", "python")

    # create virtual environment
    _print_info("Setting up virtual environment...")
    venv_options = "--clear --upgrade-deps --prompt machine"
    _exec(f"python3 -m venv {machine_venv_path} {venv_options}", silent=True)

    # install dependencies
    cmd = [python, "-m", "pip", "install", "-r", req_file, "--upgrade"]
    _exec(cmd, silent=True)
    return python


def setup(python: str, machine_path: str, config_path, *args):
    """Execute machine setup script."""
    script = os.path.join(machine_path, SCRIPT)

    if not config_path:
        _exec([python, script, *args], safe=False)
        return

    _print_info(f"Using config path: {config_path}")
    config_path = os.path.realpath(config_path) if config_path else None
    _exec([python, script, config_path, *args], safe=False)


def _print_error(error: str) -> None:
    print(f"\033[31;1m{error}\033[0m")


def _print_info(info: str) -> None:
    print(f"\033[1m{info}\033[0m")


def _exec(cmd, silent=False, safe=False, text=False):
    # execute command and return output or exit code
    options: dict = dict(check=not safe, capture_output=silent, text=text)
    result = subprocess.run(cmd, shell=isinstance(cmd, str), **options)
    return result.stdout.strip() if text else result.returncode


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap machine setup.")
    parser.add_argument("-f", "--force", action="store_true", help="overwrite")
    parser.add_argument(
        "config_path", nargs="?", type=str, help="config files path"
    )
    parser.add_argument(
        "args",
        metavar="...",
        nargs=argparse.REMAINDER,
        help="setup script arguments",
    )

    args = parser.parse_args()
    try:
        main(args.config_path, args.force, *args.args)
    except Exception as e:
        _print_error(f"Error: {e}")
        _print_error("Failed to bootstrap machine")
        exit(1)
