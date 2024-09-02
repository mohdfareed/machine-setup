#!/usr/bin/env python3
"""Bootstrap a new machine. This will clone the machine's configuration and
execute the setup script.

Requirements:
    - SETUP_SCRIPT at the root of the machine repository

External effects:
    - Clones machine into the specified path
    - Executes the setup script
"""

import argparse
import os
import shutil
import subprocess
import sys

REPO = "https://github.com/mohdfareed/machine.git"
"""URL of the repository to clone."""
SETUP_SCRIPT = "setup.sh"
"""Name of the setup script to execute."""


def main(machine: str, path: str, overwrite=False, setup_args=None) -> None:
    """Bootstrap the machine setup process."""

    # clone machine, overwrite if prompted
    print(f"Cloning machine into: {path}")
    if overwrite and os.path.exists(path):
        print("Removing existing machine...")
        shutil.rmtree(path, ignore_errors=True)
    if not os.path.exists(path):  # clone machine otherwise
        run(["git", "clone", "-q", REPO, path], silent=True)

    # execute machine setup script
    script = os.path.join(path, SETUP_SCRIPT)
    run([script, machine, *(setup_args or [])])


def run(cmd, silent=False):
    """Run a shell command."""
    subprocess.run(cmd, capture_output=silent, check=True)


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
        print(rf"\033[31;1m{'Error:'}\033[0m {e}")
        print(rf"\033[31;1m{'Failed to bootstrap machine'}\033[0m")
        sys.exit(1)
