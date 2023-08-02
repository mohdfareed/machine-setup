"""Shell module executing shell commands. The module provides a `run` function
for running shell commands and `run_quiet` for running commands without
printing their output. The provides an interactive mode of the shell.
"""

import subprocess
from typing import Callable, Optional

LOADING_STR: str = "Loading"
"""The default string to print while waiting for a command to complete. It is
followed by a loading animation.
"""

LOADING_ANIMATION: list[str] = ["", ".", "..", "..."]
"""The default loading animation used when waiting for a command to exit.
"""

SHELL: str = "/bin/zsh"
"""The default shell to use for executing commands.
"""


def run(cmd: str, printer: Callable, error: Optional[Callable] = None) -> int:
    """Runs a shell command and prints the output and errors using the
    provided `printer(str)`. Errors can be printed using a different `error`
    function.

    Args:
        cmd (str): The command to run.
        printer (function): The function used to print the output.
        error (function, optional): The function used to print errors. If
        `None`, the `printer` function is used.

    Returns:
        The exit code of the command.
    """
    error = error or printer
    process = subprocess.Popen(
        cmd,
        shell=True,
        executable=SHELL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    _print_output(process, printer, error)
    return process.returncode


def run_quiet(cmd: str, printer: Callable, loading_string=LOADING_STR) -> int:
    """Runs a shell command and waits for it to complete. A loading
    animation is printed using `builtins.print` while the command is
    running. The output of the command is printed using the provided
    `printer` function.

    Args:
        cmd (str): The command to run.
        printer (function, optional): The command outputs printer.
        loading_str (str): The loading string to print.

    Returns:
        The exit code of the command.
    """
    process = subprocess.Popen(
        cmd,
        shell=True,
        executable=SHELL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    # show loading animation
    # _loader(process.poll, loading_string)
    output = process.communicate()  # get the standard output and error

    # print the standard outputs and errors then return the exit code
    if output[0].decode().strip() != "":
        printer(cmd + "\n" + output[0].decode().strip())
    return process.returncode


def read(cmd: str) -> str:
    """Runs a shell command and returns the standard output.

    Args:
        cmd (str): The command to run.

    Returns:
        The standard output of the command.

    Raises:
        RuntimeError: If the command failed.
    """
    process = subprocess.run(cmd, capture_output=True, shell=True)
    if process.returncode != 0:
        error = process.stderr.decode().strip()
        raise RuntimeError("Command failed: " + cmd + "\n" + error)
    return process.stdout.decode().strip()


# def interactive() -> None:
#     """Runs the shell in interactive mode. No output is logged when running in
#     this mode. The shell used is the default shell of the module.
#     """
#     from .colors import bright_blue as blue
#     from .colors import bright_green as green
#     from .colors import bright_red as red
#     from .logger import Display

#     display = Display(no_logging=True)
#     print("Shell interface written in Python. Shell: " + SHELL)
#     print(blue("Type 'exit' to stop.\n"))

#     exit_code = 0
#     while True:
#         # print prompt based on the exit code of the previous command
#         if exit_code != 0:
#             print(red("> "), end="")
#         else:
#             print(green("> "), end="")
#         # read a command and break if it is "exit"
#         cmd = input()
#         if cmd == "exit":
#             break

#         # run the command and print output
#         exit_code = run(cmd, display.print, display.error)


# def _loader(condition, loading_string):
#     """Prints a loading animation until `condition` does not return `None`. The
#     loading animation is printed using the provided `loading_string`.

#     Args:
#         condition (function): The function that returns `None` to stop.
#         loading_string (str): The loading string to print.
#     """
#     import time

#     time.sleep(0.05)  # wait for the process to start

#     counter = 0
#     while condition() is None:
#         # print the loading string and animation
#         print(loading_string + LOADING_ANIMATION[counter])
#         # wait after printing the animation for 1 second
#         time.sleep(1 / len(LOADING_ANIMATION))
#         # clear the line and increment the counter
#         print(LINE_UP + LINE_CLEAR + LINE_UP)
#         counter = (counter + 1) % len(LOADING_ANIMATION)


def _print_output(process, printer, error_printer):
    """Prints the output of a process line by line until the process
    completes.

    Args:
        process (subprocess.Popen): The process to print the output of.
        printer (function): The printer of the standard output.
        error_printer (function): The printer of the standard error.
    """

    output, error = "", ""
    while True:
        # read a line from the process's output and error
        if process.stdout is not None:
            output = process.stdout.readline().decode().strip()
        if process.stderr is not None:
            error = process.stderr.readline().decode().strip()

        # print the output if it is not empty
        if output:
            printer(output)
        # print the error if it is not empty
        if error:
            error_printer(error)

        # break if the process has completed and there is no output
        if process.poll() is not None and not (output or error):
            break


def __getattr__(name):
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# if __name__ == "__main__":
#     print("Running shell in interactive mode.\n")
#     interactive()
