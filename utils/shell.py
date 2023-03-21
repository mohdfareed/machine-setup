"""Shell module that contains a `Shell` class for executing shell commands. It
either prints the output of the command to a provided function or prints a
loading animation while the command is running.
"""

import subprocess
from typing import Callable

LOADING_STR: str = "Loading"
"""The default string to print while waiting for a command to complete. It is
followed by a loading animation.
"""

LOADING_ANIMATION: list[str] = ["", ".", "..", "..."]
"""The default loading animation used when waiting for a command to exit.
"""


class Shell:
    """Shell class that provides functions for executing shell commands.
    Commands can be executed in a verbose or quiet mode. The verbose mode
    prints the outputs to a provided `printer` function. The quiet mode prints
    a loading animation while the command is running and prints the output to
    a provided function.
    """

    def __init__(self, shell: str = "/bin/zsh") -> None:
        """Create a new Shell object with the provided shell command.

        Args:
            shell (str): The shell to use for commands execution.
        """
        self.shell = shell
        """The shell to use for commands execution.
        """

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
                  loading_printer: Callable = print,
                  loading_string: str = LOADING_STR) -> int:
        """Runs a shell command and waits for it to complete. A loading
        animation is printed to `loading_printer` while the command is running.
        The output of the command is printed using the provided `printer`
        function. Printers should not both print to the same stream.

        Args:
            cmd (str): The command to run.
            printer (function): The standard output and error printer.
            loading_printer (function, optional): The loading animation printer.
            loading_str (str): The loading string to print.

        Returns:
            The exit code of the command.
        """
        process = subprocess.Popen(cmd, shell=True, executable=self.shell,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)

        # show loading animation
        _loader(process.poll, loading_printer, loading_string)
        output = process.communicate()  # get the standard output and error

        # print the standard outputs and errors then return the exit code
        if output[0].decode().strip() != "":
            printer(output[0].decode().strip())
        printer(loading_string + " done.")  # print completion indicator
        return process.returncode

    def interactive(self) -> None:
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
                 loading_printer: Callable = print,
                 loading_string: str = LOADING_STR) -> int:
        return self.run_quiet(cmd, printer, loading_printer, loading_string)


def _loader(condition: Callable,
            loading_printer: Callable, loading_string: str) -> None:
    """Prints a loading animation until `condition` does not return `None`. The
    loading animation is printed using the provided `loading_string`. When the
    animation stops, the `loading_string` is printed followed by " done.".

    Args:
        condition (function): The function that returns `None` to stop.
        loading_printer (function): The printer of the loading animation.
        loading_string (str): The loading string to print.
    """
    import time
    time.sleep(0.05)  # wait for the process to start

    counter = 0
    while condition() is None:
        # print the loading string and animation
        complete_string = loading_string + LOADING_ANIMATION[counter]
        loading_printer(complete_string + "\r")
        # wait after printing the animation for 1 second
        time.sleep(1 / len(LOADING_ANIMATION))
        # clear the line and increment the counter
        print(" " * len(complete_string) + "\r")
        counter = (counter + 1) % len(LOADING_ANIMATION)
    print(loading_string + " done.")


def _print_process_output(process: subprocess.Popen,
                          printer: Callable, error_printer: Callable) -> None:
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
