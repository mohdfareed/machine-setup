#!/usr/bin/env python3

from utils import shell
from utils.display import Display


def update(display: Display) -> None:
    """Run the main function of the setup script. This function is called when
    the script is run from the command line.

    Args:
        display (Display): The display for printing messages.
    """
    display.header("Updating machine...")

    # get resources if not already present
    display.debug("Initializing resources...")
    cmd = 'git submodule update --init --recursive --remote'
    if shell.run_quiet(cmd, display.verbose, "Initializing resources") != 0:
        raise RuntimeError("Failed to initialize resources.")
    display.success("Resources initialized.")

    # run setup modules
    display.debug("Running update modules...")
    _invoke_update(display)
    display.success("")
    display.success("Machine update complete!")
    display.info("Please restart your machine for some changes to apply.")


def main() -> None:
    """Initialize the Display and run the main update function.
    """
    import argparse

    # parse command line arguments
    parser = argparse.ArgumentParser(description="Machine setup script.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print verbose messages, including commands")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="print debug messages")
    parser.add_argument("--no-logging", action="store_true",
                        help="don't log output to a file")
    args = parser.parse_args()

    # create a display instance for logging and printing messages
    verbose, debug, no_logging = args.verbose, args.debug, args.no_logging
    display = _init(verbose, debug, no_logging)

    try:  # run main function and handle exceptions
        update(display)
    except Exception as exception:
        display.error(exception.__str__())
        display.error("")
        display.error(f"Failed to update machine.")


def _init(verbose, debug, no_logging) -> Display:
    """Initialize the display for printing messages and logging them to a file.
    """
    display = Display(verbose, debug, no_logging)
    display.debug("Debug mode is enabled.") if debug else None
    display.verbose("Verbose mode is enabled.") if verbose else None
    display.info("Logging is disabled.") if no_logging else None
    return display


def _invoke_update(display: Display) -> None:
    """Invoke the update modules.

    Args:
        display (Display): The display for printing messages.
    """
    from core import git, homebrew, macos, python, zsh

    # homebrew.update(display)
    # zsh.update(display)
    # git.update(display)
    # python.update(display)
    # macos.update(display)


if __name__ == "__main__":
    main()
