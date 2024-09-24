#!/usr/bin/env python3
"""Bootstrap a new machine. This will clone the machine's configuration and
execute the setup script."""

import argparse
import os
import platform
import shutil
import subprocess
import sys
from typing import Optional

REPOSITORY = "https://github.com/mohdfareed/machine.git"

# the script to execute for machine setup
MODULE = "machines.{}.setup"
DEFAULT_MACHINE = "codespaces" if os.environ.get("CODESPACES") else "dummy"
DEFAULT_MACHINE_PATH = os.environ.get("MACHINE") or os.path.join(
    os.path.expanduser("~"), ".machine"
)  # default to $MACHINE or ~/.machine


def main(
    machine: str = DEFAULT_MACHINE,
    path: str = DEFAULT_MACHINE_PATH,
    overwrite: bool = False,
    setup_args: Optional[list[str]] = None,
):
    """Bootstrap the machine setup process."""
    path = os.path.realpath(path)
    if not machine:
        raise ValueError("Machine name not provided.")

    _clone_machine(path, overwrite)
    python = _create_virtual_env(path, machine, overwrite)
    _install_dependencies(python, path)
    _setup_machine(python, f"machines.{machine}.setup", path, setup_args)


def _clone_machine(path: str, clean: bool):
    if clean and os.path.exists(path):  # remove existing
        _log_info("Removing existing machine...")
        shutil.rmtree(path, ignore_errors=True)
    if not os.path.exists(path):  # clone if not exists
        _log_info("Cloning machine repository...")
        subprocess.run(["git", "clone", "-q", REPOSITORY, path], check=True)
    else:
        _update_machine(path)


def _update_machine(path: str):
    if subprocess.run(["git", "diff", "--quiet"], cwd=path, check=False).returncode != 0:
        _log_warning("Uncommitted changes found. Skipping update.")
        return

    _log_info("Updating machine...")  # pull latest changes
    subprocess.run(["git", "pull"], cwd=path, check=True)


def _create_virtual_env(path: str, prompt: str, clean: bool) -> str:
    venv = os.path.join(path, ".venv")
    if clean and os.path.exists(venv):  # remove existing
        _log_info("Removing existing environment...")
        shutil.rmtree(path, ignore_errors=True)

    if not os.path.exists(venv):  # skip if exists
        _log_info("Creating virtual environment...")
        opts = ["--clear", "--prompt", prompt, "--upgrade-deps"]
        subprocess.run(["python3", "-m", "venv", *opts, venv], check=True)
    else:
        _log_warning("Virtual environment already exists. Skipping creation.")

    bin_path = "bin" if platform.system() != (_ := "Windows") else "Scripts"
    return os.path.join(venv, bin_path, "python")


def _install_dependencies(python: str, path: str):
    req_file = os.path.join(path, "requirements.txt")
    cmd = [python, "-m", "pip", "install", "-r", req_file, "--upgrade"]
    _log_info("Installing dependencies...")
    subprocess.run(cmd, capture_output=True, check=True)


def _setup_machine(python: str, module: str, path: str, setup_args: Optional[list[str]] = None):
    script_path = os.path.join(path, *module.split(".")) + ".py"
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Machine script not found: {script_path}")

    setup = [python, "-m", module, *(setup_args or [])]
    _log_info("Bootstrapping machine...")
    subprocess.run(setup, cwd=path, check=False)


def _log_error(msg: str):
    print(f"\033[31m{'ERROR'}\033[0m    {msg}")


def _log_success(msg: str):
    print(f"\033[35m{'SUCCESS'}\033[0m  {msg}")


def _log_warning(msg: str):
    print(f"\033[33m{'WARNING'}\033[0m  {msg}")


def _log_info(msg: str):
    print(f"\033[34m{'INFO'}\033[0m     {msg}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Bootstrap a new machine.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="overwrite machine if it exists",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="the path to the machine repo",
        default=DEFAULT_MACHINE_PATH,
    )
    parser.add_argument(
        "machine",
        type=str,
        help="the machine to bootstrap",
        nargs="?",
        default=DEFAULT_MACHINE,
    )
    parser.add_argument("args", nargs=argparse.REMAINDER, help="additional setup arguments")

    # parse arguments
    args = parser.parse_args()
    force = args.force
    machine_path = args.path
    machine_name = args.machine
    additional_args = args.args

    try:
        main(machine_name, machine_path, force, additional_args)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:  # pylint: disable=broad-except
        _log_error(f"{e}")
        print(f"\033[31;1m{'Failed to bootstrap machine.'}\033[0m")
        sys.exit(1)
    _log_success("Machine was bootstrapped successfully.")
