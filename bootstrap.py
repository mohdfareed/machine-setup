#!/usr/bin/env python3
"""Bootstrap a new machine. This will install Xcode Commandline Tools, accept
the Xcode license, clone machine, and execute the setup script.

Requirements: Xcode Commandline Tools
Usage: ./deploy.sh local_config_path
 - local_config_path: path to local config file, which contains two files:
   - `machine.sh`: machine-specific environment, includes `MACHINE`
   - `raspberrypi.sh`: raspberry pi environment, includes `MACHINE`
The environment variable `MACHINE` is the path to the machine repo.

External effects:
  - Accepts Xcode license
  - Clones machine to `~/Developer/machine`
  - Creates a virtual environment at `~/Developer/machine/.venv`
  - Executes `setup.sh` in machine
"""

import os
import shutil
import subprocess
import sys
import venv

REQUIREMENTS = "requirements.txt"
"""Virtual environment requirements filename."""
VENV_PATH = ".venv"
"""Path to the virtual environment."""
REPOSITORY = "mohdfareed/machine.git"
"""Repository to clone."""


def main(config_path: str, clean=False, log=True, debug=False) -> None:
    """Clone and set up machine."""
    # check xcode and accept license
    resolve_xcode()

    # load machine path
    config_path = os.path.realpath(config_path)
    machine_path = load_machine_path(config_path)

    # clone repository
    clone_machine(machine_path)
    # setup virtual environment
    python = setup_env(machine_path, clean)

    # start machine setup
    cmd = setup_command(log, debug, config_path)
    os.system(f"cd '{machine_path}' && '{python}' {cmd}")


def resolve_xcode():
    # check if xcode commandline tools are installed
    if os.system("xcode-select -p > /dev/null 2>&1"):
        _print_error("Xcode Commandline Tools are not installed")
        sys.exit(1)

    # accept xcode license
    prompt = "Authenticate to accept Xcode license agreement: "
    os.system(f"sudo --prompt '{prompt}' xcodebuild -license accept")


def load_machine_path(config_path: str) -> str:
    # resolve config/machine.sh
    machine_env = os.path.join(config_path, "machine.sh")
    if not os.path.exists(machine_env):
        _print_error(f"Machine file not found at: {machine_env}")
        sys.exit(1)

    # read MACHINE from config/machine.sh
    command = f"source '{machine_env}' && echo $MACHINE"
    machine_path = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, text=True
    ).stdout.strip()
    return machine_path


def clone_machine(path: str):
    # prompt for cloning machine if it already exists
    if os.path.exists(path):
        print(f"Machine directory already exists at: {path}")
        answer = input("Do you want to overwrite it? (y|N) ")
        if not answer.lower() in ["y", "yes"]:
            return

    # clone machine
    _print_info(f"Cloning machine into '{path}'...")
    shutil.rmtree(path, ignore_errors=True)
    os.system(f"git clone -q '{REPOSITORY}' '{path}'")


def setup_env(machine_path: str, clean: bool) -> str:
    requirements_path = os.path.join(machine_path, REQUIREMENTS)
    machine_venv_path = os.path.join(machine_path, VENV_PATH)
    python = os.path.join(machine_venv_path, "bin", "python")

    # create virtual environment
    _print_info("Creating environment...")
    env_options = dict(clear=clean, with_pip=True, upgrade_deps=True)
    venv.create(machine_venv_path, prompt="setup", **env_options)

    # install dependencies
    cmd = f"{python} -m pip install -r '{requirements_path}' --upgrade"
    os.system(f"{cmd} > /dev/null 2>&1")
    return python


def setup_command(log, debug, config_path):
    log = "--log" if log else ""
    debug = "--debug" if debug else ""
    return f"./setup.py {log} {debug} '{config_path}'"


def _print_error(error: str) -> None:
    print(f"\033[31;1m{error}\033[0m")


def _print_info(info: str) -> None:
    print(f"\033[1m{info}\033[0m")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Bootstrap machine.")
    parser.add_argument(
        "config_path", nargs="?", type=str, help="local machine config path"
    )
    parser.add_argument(
        "-c", "--clean", action="store_true", help="clean setup environment"
    )
    parser.add_argument(
        "-l", "--log", action="store_true", help="log messages to file"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="log debug messages"
    )

    args = parser.parse_args()
    main(args.config_path, args.clean, args.log, args.debug)
