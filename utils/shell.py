"""Shell module that contains a `Shell` class for executing shell commands. It
either prints the output of the command to a provided function or prints a
loading animation while the command is running.
"""

import subprocess
from typing import Callable

LOADING_STR: str = "Loading"
"""The default string to print while waiting for a command to complete. It is
followed by a loading animation."""


class Shell:
    """Shell class that provides functions for executing shell commands.
    Commands can be executed in a verbose or quiet mode. The verbose mode
    prints the outputs to a provided `printer` function. The quiet mode prints
    a loading animation while the command is running and prints the output to
    a provided function.
    """

    def __init__(self, shell: str = "/bin/zsh"):
        """Create a new Shell object with the provided shell command.

        Args:
            shell (str): The shell to use for commands execution.
        """
        self.shell = shell
        """The shell to use for commands execution."""

    def run(self, cmd: str, printer: Callable, error_printer: Callable) -> int:
        """Runs a shell command and prints the output and errors using the
        provided `printer` and `error_printer` functions.

        The `printer` and `error_printer` functions should take a string as an
        argument.

        Args:
            cmd (str): The command to run.
            printer (function): The function used to print the output.
            error_printer (function): The function used to print errors.

        Returns:
            The exit code of the command.
        """
        process = subprocess.Popen(cmd, shell=True, executable=self.shell,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        _print_process_output(process, printer, error_printer)
        return process.returncode

    def run_quiet(self, cmd: str, printer: Callable,
                  loading_string: str = LOADING_STR) -> int:
        """Runs a shell command and waits for it to complete. A loading
        animation is printed while the command is running. The output of the
        command is printed using the provided `printer` function. The printer
        should not print to the standard output.

        Args:
            cmd (str): The command to run.
            printer (function): The printer function which accepts a string.
            loading_str (str): The loading string to print.

        Returns:
            The exit code of the command.
        """
        process = subprocess.Popen(cmd, shell=True, executable=self.shell,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)

        _loader(process.poll, loading_string)  # show loading animation
        output = process.communicate()  # get the standard output and error

        # print the standard outputs and errors then return the exit code
        if output[0].decode().strip() != "":
            printer(output[0].decode().strip())
        return process.returncode

    def interactive(self):
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
            exit_code = self.run_quiet(command, Display(no_logging=True).debug)

    def __call__(self, cmd: str, printer: Callable,
                 loading_string: str = LOADING_STR) -> int:
        return self.run_quiet(cmd, printer, loading_string)


def _loader(condition: Callable, loading_string):
    """Prints a loading animation until `condition` does not return `None`.

    Args:
        condition (function): The function that returns `None` to stop.
    """
    import time
    time.sleep(0.05)

    counter = 0
    while condition() is None:
        # print the loading string and animation
        print(loading_string + "." * counter, end='\r')
        time.sleep(0.25)  # wait to print the next frame
        # clear the line and increment the counter
        print(" " * (len(loading_string) + counter), end='\r')
        counter = (counter + 1) % 4


def _print_process_output(process: subprocess.Popen,
                          printer: Callable, error_printer: Callable):
    """Prints the output of a process line by line until the process
    completes.

    Args:
        process (subprocess.Popen): The process to print the output of.
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
        # break if the process has completed and there is no output
        if process.poll() is not None and not (stdout or stderr):
            break


def __getattr__(name):
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


if __name__ == "__main__":
    Shell().interactive()
