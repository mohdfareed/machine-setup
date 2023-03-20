"""Shell module that provides functions for executing shell commands. Commands
can be executed in a verbose or quiet mode. The verbose mode prints the outputs
to a provided `printer` function. The quiet mode prints a loading animation
while the command is running and prints the output to a provided function.
"""

import subprocess
from typing import Callable

shell: str = "/bin/zsh"
"""The shell to use for commands execution."""

loading_string: str = "Loading"
"""The string to print while waiting for a command to complete. It is followed
by a loading animation."""


def run(cmd: str, printer: Callable, error_printer: Callable) -> int:
    """Runs a shell command and prints the output and errors using the provided
    `printer` and `error_printer` functions.

    The `printer` and `error_printer` functions should take a string as an
    argument.

    Args:
        cmd (str): The command to run.
        printer (function): The function used to print the output.
        error_printer (function): The function used to print errors.

    Returns:
        The exit code of the command.
    """
    process = subprocess.Popen(cmd, shell=True, executable=shell,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    _print_process_output(process, printer, error_printer)
    return process.returncode


def run_quiet(cmd: str, loader: Callable, printer: Callable) -> int:
    """Runs a shell command and waits for it to complete. A loader method is
    executed while the command is running. The output of the command is printed
    to the provided `printer` function.

    The `loader` function should take a `Callable` as an argument. It should
    only return when the `Callable` does not return `None`.
    The `printer` function should take a string as an argument.

    Args:
        cmd (str): The command to run.
        loader (function): The loading function which accepts a `Callable`.
        printer (function): The loading function which accepts a `Callable`.

    Returns:
        The exit code of the command.
    """
    process = subprocess.Popen(cmd, shell=True, executable=shell,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

    loader(process.poll)  # load while the process is running
    output = process.communicate()  # get the standard output and error
    printer(output[0].decode())  # print the standard output
    return process.returncode  # return the exit code


def interactive():
    """Runs the shell in interactive mode.
    """
    from utils.display import Display
    from .colors import red
    print("Shell interface written in Python. Type 'exit' to stop.")

    exit_code = 0
    while True:
        # print prompt based on the exit code of the previous command
        if exit_code != 0:
            print(red("> "), end="")
        else:
            print("> ", end="")
        # read a command and break if it is "exit"
        command = input()
        if command == "exit":
            break
        # run the command and print output
        # exit_code = run(command, print, print)
        exit_code = run_quiet(command, loader, Display(no_logging=True).debug)


def loader(condition: Callable):
    """Prints a loading animation until `condition` does not return `None`.

    Args:
        condition (function): The function that must not return `None` to stop.
    """
    import time
    time.sleep(0.05)

    counter = 0
    while condition() is None:
        print(loading_string + "." * counter, end='\r')
        time.sleep(0.25)
        print(" " * (len(loading_string) + counter), end='\r')
        counter = (counter + 1) % 4


def _print_process_output(process: subprocess.Popen, printer: Callable,
                          error_printer: Callable):
    """Prints the output of a process line by line until the process
    completes.

    Args:
        process (subprocess.Popen): The process of which the output is printed.
        printer (function): The printer of the standard output.
        error_printer (function): The printer of the standard error.
    """

    stdout = stderr = ""
    while True:
        # read a line from the process's output and error
        if process.stdout is not None:
            stdout = process.stdout.readline().decode().strip()
        if process.stderr is not None:
            stderr = process.stderr.readline().decode().strip()
        # print the output and error if they are not empty
        if stdout:
            printer(stdout)
        if stderr:
            error_printer(stderr)
        # break if the process has completed and there is no output or error
        if process.poll() is not None and not (stdout or stderr):
            break


def __getattr__(name):
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


if __name__ == "__main__":
    interactive()
