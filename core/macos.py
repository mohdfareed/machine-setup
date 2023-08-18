"""Setup module containing a `setup` function for setting up Git on a new
machine."""

import config
import utils

printer = utils.Printer("macos")
"""The macOS setup printer."""
shell = utils.Shell(printer.debug, printer.error)
"""The macOS shell instance."""


def setup() -> None:
    """Setup macOS on a new machine."""
    printer.info("Setting up macOS...")

    # add terminal profiles
    # shell(["open", "-g", config.terminal_dark], silent=True)
    # shell(["open", "-g", config.terminal_light], silent=True)
    # printer.debug("Added terminal profiles")

    # run the preferences script
    printer.print("Setting system preferences...")
    shell(f". {config.macos_preferences}")

    # update the system
    printer.print("Updating the system...")
    shell("softwareupdate --install --all")
    printer.success("macOS setup complete")


if __name__ == "__main__":
    import argparse

    import core

    parser = argparse.ArgumentParser(description="macOS setup script.")
    args = parser.parse_args()
    core.run(setup, printer, "Failed to setup macOS")
