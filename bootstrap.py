#!/usr/bin/env python3
"""Bootstrap a new machine. This will clone the machine's configuration and
execute the setup script.

Requirements:
    - Python 3.7+
    - git must be installed
    - setup script at the root of the machine repository

External effects:
    - Clones machine into the specified path
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
SETUP_SCRIPT = "setup.sh"
"""Name of the setup script to execute."""
SETUP_SCRIPT_WINDOWS = "setup.ps1"
"""Name of the setup script for Windows."""


def main(path: str, overwrite=False, setup_args=None) -> None:
    """Bootstrap the machine setup process."""

    # Determine the appropriate setup script based on the OS
    windows_platform = "Windows"
    is_windows = platform.system() == windows_platform
    setup_script = SETUP_SCRIPT_WINDOWS if is_windows else SETUP_SCRIPT
    setup_script = os.path.join(path, setup_script)

    # remove existing machine if requested
    if overwrite and os.path.exists(path):
        print("Removing existing machine...")
        shutil.rmtree(path, ignore_errors=True)

    # clone machine if it doesn't exist
    print(f"Cloning machine into: {path}")
    if not os.path.exists(path):  # clone machine otherwise
        subprocess.run(["git", "clone", "-q", REPO, path], check=True)

    # execute machine setup script
    print(f"Executing setup script: {setup_script}")
    if not is_windows:
        subprocess.run([setup_script, *(setup_args or [])], check=True)
    else:
        subprocess.run(
            [
                "powershell",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                setup_script,
                *(setup_args or []),
            ],
            check=True,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap a new machine.")
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
    parser.add_argument(
        "args", nargs=argparse.REMAINDER, help="additional setup arguments"
    )

    # parse arguments
    args = parser.parse_args()
    machine_path = args.path
    force = args.force
    additional_args = args.args

    try:
        main(machine_path, force, additional_args)
    except Exception as e:  # pylint: disable=broad-except
        print(f"\033[31;1m{'Error:'}\033[0m {e}")
        print(f"\033[31;1m{'Failed to bootstrap machine.'}\033[0m")
        sys.exit(1)
