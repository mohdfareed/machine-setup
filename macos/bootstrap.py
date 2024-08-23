#!/usr/bin/env python3
"""Bootstrap a new macOS machine. This will clone machine configuration and
execute the setup script.

Requirements: Xcode Commandline Tools.

External effects:
  - Accepts Xcode license
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
SHELL_ENV = (
    "https://raw.githubusercontent.com/mohdfareed/machine/main/macos/zshenv"
)
"""URL of the shell environment file."""

SCRIPT = "macos/setup.py"
"""Machine setup script filename."""
REQUIREMENTS = "requirements.txt"
"""Virtual environment requirements filename."""
VENV = ".venv"
"""Path to the virtual environment."""


def main(overwrite=False, verbose=False) -> None:
    """Bootstrap the machine setup process."""

    prompt = "Authenticate to accept Xcode license agreement: "
    try:  # accept xcode license
        run(["sudo", "--prompt", prompt, "xcodebuild", "-license", "accept"])
    except subprocess.CalledProcessError as ex:
        raise RuntimeError(
            "Failed to accept Xcode license."
            "Ensure Xcode is installed using: xcode-select --install"
        ) from ex

    # resolve machine path
    with urllib.request.urlopen(SHELL_ENV) as response:
        env_file = response.read().decode()
    machine_path = run(f"{env_file} \n echo $MACHINE", silent=True, text=True)
    machine_path = os.path.realpath(machine_path)

    # resolve environment paths
    req_file = os.path.join(machine_path, REQUIREMENTS)
    machine_venv_path = os.path.join(machine_path, VENV)
    python = os.path.join(machine_venv_path, "bin", "python")

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
    run(f"python3 -m venv {machine_venv_path} {venv_options}", silent=True)
    cmd = [python, "-m", "pip", "install", "-r", req_file, "--upgrade"]
    run(cmd, silent=True)  # install dependencies

    # execute machine setup script
    script = os.path.join(machine_path, SCRIPT)
    command = f"{script}{' -d' if verbose else ''}"
    run([python, command], safe=False)


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
        "-f",
        "--force",
        action="store_true",
        help="overwrite machine if it exists",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print verbose output",
    )
    # parser.add_argument(
    #     "-m",
    #     "--machine",
    #     type=str,
    #     choices=["macos", "rpi"],
    #     help="specify the type of machine to setup",
    # )
    args = parser.parse_args()

    try:
        main(args.force, args.verbose)
    except Exception as e:  # pylint: disable=broad-except
        print(f"\033[31;1m{'Error:'}\033[0m {e}")
        print(f"\033[31;1m{'Failed to bootstrap machine'}\033[0m")
        sys.exit(1)
    try:
        main(True)
    except Exception as e:  # pylint: disable=broad-except
        print(f"\033[31;1m{'Error:'}\033[0m {e}")
        print(f"\033[31;1m{'Failed to bootstrap machine'}\033[0m")
        sys.exit(1)
