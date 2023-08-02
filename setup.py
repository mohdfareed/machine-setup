#!/usr/bin/env python3

import config
import core
import utils
import os

printer = utils.Printer("setup")
"""the main setup printer."""


def main(config_path: str, log=False, debug=False) -> None:
    """Setup the machine.

    Args:
        config_path (str): Path to the local config directory.
        log (bool): Whether to log output to a file.
        debug (bool): Whether to log debug messages.
    """

    # initial setup
    config_path = utils.abspath(config_path)
    os.chdir(os.path.dirname(utils.abspath(__file__)))
    utils.Printer.initialize(to_file=log, debug=debug)

    try:  # setup the machine
        setup_machine(config_path)
    except Exception as exception:
        printer.logger.exception(exception)  # log exception
        printer.error("Failed to setup machine.")


def setup_machine(config_path: str) -> None:
    """Run the main function of the setup script. This function is called when
    the script is run from the command line.

    Args:
        display (Display): The display for printing messages.
        ssh_dir (str): The path to the SSH directory of keys.
    """

    printer.title("Setting up machine...")
    # symlink environment files
    utils.symlink(utils.abspath(config_path, "machine.sh"), config.zshenv)
    utils.symlink(
        utils.abspath(config_path, "pi.sh"), config.raspberrypi_zshenv
    )

    # run setup scripts
    # homebrew.setup()
    # zsh.setup()
    # ssh.setup()
    # git.setup()
    # python.setup()
    # macos.setup()
    # core.raspberrypi.setup()

    printer.info("Restart for some changes to apply")
    printer.success("Machine setup complete")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Setup machine.")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="start in debug mode"
    )
    parser.add_argument(
        "-l", "--log", action="store_true", help="log to a file"
    )
    parser.add_argument(
        "config_path", nargs="?", type=str, help="local machine config path"
    )

    args = parser.parse_args()
    main(args.config_path, args.log, args.debug)
