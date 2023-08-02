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
import sys
import venv

REPOSITORY = "https://github.com/mohdfareed/machine.git"
"""Repository to clone."""
SCRIPT = "setup.py"
"""Machine setup script filename."""
REQUIREMENTS = "requirements.txt"
"""Virtual environment requirements filename."""
VENV_PATH = ".venv"
"""Path to the virtual environment."""


def main(config_path: str, overwrite=False, *args) -> None:
    """Clone and set up machine."""

    machine_path = load_machine_path(config_path)   # load machine path
    resolve_xcode()                                 # resolve xcode license
    clone_machine(machine_path, overwrite)          # clone repository
    python = setup_env(machine_path)                # setup virtual environment
    setup(python, machine_path, config_path, *args) # setup machine


def load_machine_path(config_path: str) -> str:
    # resolve config/machine.sh
    machine_env = os.path.realpath(os.path.join(config_path, "machine.sh"))
    if not os.path.isfile(machine_env):
        _print_error(f"Machine file not found at: {machine_env}")
        sys.exit(1)

    # read MACHINE from config/machine.sh
    command = f"source '{machine_env}' && echo $MACHINE"
    machine_path = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, text=True, check=True
    ).stdout.strip()
    return os.path.abspath(machine_path) # don't follow symlinks


def resolve_xcode():
    try:  # check if xcode commandline tools are installed
        subprocess.run(["xcode-select", "-p"], check=True)
    except subprocess.CalledProcessError:
        _print_error("Xcode Commandline Tools are not installed")
        sys.exit(1)

    # accept xcode license
    prompt = "Authenticate to accept Xcode license agreement: "
    cmd = ["sudo", "--prompt", prompt, "xcodebuild", "-license", "accept"]
    subprocess.run(cmd, check=True)


def clone_machine(path: str, overwrite=False):
    # overwrite machine if prompted
    if os.path.exists(path) and overwrite:
        _print_info(f"Overwriting machine...")
        shutil.rmtree(path, ignore_errors=True)

    # clone machine
    _print_info(f"Cloning machine into '{path}'...")
    subprocess.run(["git", "clone", "-q", REPOSITORY, path], check=True)


def setup_env(machine_path: str) -> str:
    req_path = os.path.join(machine_path, REQUIREMENTS)
    machine_venv_path = os.path.join(machine_path, VENV_PATH)
    python = os.path.join(machine_venv_path, "bin", "python")

    # create virtual environment
    _print_info("Creating environment...")
    env_options = dict(with_pip=True, upgrade_deps=True)
    venv.create(machine_venv_path, prompt="setup", **env_options)

    # install dependencies
    cmd = [python, "-m", "pip", "install", "-r", req_path, "--upgrade"]
    subprocess.run(cmd, check=True)
    return python


def setup(python: str, machine_path: str, config_path: str, *args):
    """Execute machine setup script."""
    script = os.path.join(machine_path, SCRIPT)
    subprocess.run([python, script, config_path, *args])


def _print_error(error: str) -> None:
    print(f"\033[31;1m{error}\033[0m")


def _print_info(info: str) -> None:
    print(f"\033[1m{info}\033[0m")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap machine setup.")
    parser.add_argument(
        "config_path", nargs="?", type=str, help="local machine config path"
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="overwrite repo and venv"
    )
    parser.add_argument(
        "args", nargs=argparse.REMAINDER, help="setup script arguments"
    )

    args = parser.parse_args()
    main(args.config_path, args.overwrite, args.args)
