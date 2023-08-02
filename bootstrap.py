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

    machine_path = load_machine_path(config_path)  # load machine path
    resolve_xcode()  # resolve xcode license
    clone_machine(machine_path, overwrite)  # clone repository
    python = setup_env(machine_path)  # setup virtual environment
    setup(python, machine_path, config_path, *args)  # setup machine


def load_machine_path(config_path: str) -> str:
    # resolve config/machine.sh
    machine_env = os.path.realpath(os.path.join(config_path, "machine.sh"))
    if not os.path.isfile(machine_env):
        _print_error(f"Machine file not found at: {machine_env}")
        exit(1)

    # read MACHINE from config/machine.sh
    command = f"source '{machine_env}' && echo $MACHINE"
    machine_path = _exec(command, silent=True, text=True)
    _print_info(f"Loaded machine path: {machine_path}")
    return os.path.abspath(machine_path)  # don't follow symlinks


def resolve_xcode():
    try:  # check if xcode commandline tools are installed
        _exec("xcode-select -p", silent=True)
    except subprocess.CalledProcessError:
        _exec("xcode-select --install", silent=True)  # prompt to install
        _print_error("Xcode Commandline Tools are not installed")
        exit(1)

    # accept xcode license
    prompt = "Authenticate to accept Xcode license agreement: "
    _exec(["sudo", "--prompt", prompt, "xcodebuild", "-license", "accept"])


def clone_machine(path: str, overwrite=False):
    # overwrite machine if prompted
    if overwrite and os.path.exists(path):
        _print_info(f"Overwriting machine...")
        shutil.rmtree(path, ignore_errors=True)

    if not os.path.exists(path):  # clone machine
        _print_info(f"Cloning machine into '{path}'...")
        _exec(["git", "clone", "-q", REPOSITORY, path], silent=True)


def setup_env(machine_path: str) -> str:
    req_path = os.path.join(machine_path, REQUIREMENTS)
    machine_venv_path = os.path.join(machine_path, VENV_PATH)
    python = os.path.join(machine_venv_path, "bin", "python")

    # create virtual environment
    _print_info("Setting up virtual environment...")
    env_options = dict(with_pip=True, upgrade_deps=True)
    venv.create(machine_venv_path, prompt="setup", **env_options)

    # install dependencies
    cmd = [python, "-m", "pip", "install", "-r", req_path, "--upgrade"]
    _exec(cmd, silent=True)
    return python


def setup(python: str, machine_path: str, config_path: str, *args):
    """Execute machine setup script."""
    script = os.path.join(machine_path, SCRIPT)
    _exec([python, script, config_path, *args], safe=False)


def _print_error(error: str) -> None:
    print(f"\033[31;1m{error}\033[0m")


def _print_info(info: str) -> None:
    print(f"\033[1m{info}\033[0m")


def _exec(cmd: str | list, silent=False, safe=False, text=False):
    # execute command and return output or exit code
    options: dict = dict(check=not safe, capture_output=silent, text=text)
    result = subprocess.run(cmd, shell=isinstance(cmd, str), **options)
    return result.stdout.strip() if text else result.returncode


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap machine setup.")
    parser.add_argument(
        "config_path", nargs="?", type=str, help="local machine config path"
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="overwrite repo and venv"
    )
    parser.add_argument(
        "...", nargs=argparse.REMAINDER, help="setup script arguments"
    )

    args = parser.parse_args()
    try:
        main(args.config_path, args.overwrite, *args.args)
    except:
        _print_error("Failed to bootstrap machine")
        exit(1)
