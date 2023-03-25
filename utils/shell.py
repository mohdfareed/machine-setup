"""Shell module that contains a `Shell` class for executing shell commands. The
module provides an interactive mode of the shell that can be used in the
terminal. This modules also holds the default loading string and animation used
by any instance of the `Shell` class.
"""

import subprocess
from typing import Callable
from utils.display import Display

LOADING_STR: str = "Loading"
"""The default string to print while waiting for a command to complete. It is
followed by a loading animation.
"""

LOADING_ANIMATION: list[str] = ["", ".", "..", "..."]
"""The default loading animation used when waiting for a command to exit.
"""

SHELL: str = '/bin/zsh'
"""The default shell to use for executing commands.
"""

_LINE_UP = '\033[1A'
"""The ANSI escape sequence for moving the cursor up one line."""
_LINE_CLEAR = '\x1b[2K'
"""The ANSI escape sequence for clearing the current line."""


class Shell:
    """Shell class that provides functions for executing shell commands.
    Commands can be executed in a verbose or quiet mode. The verbose mode
    prints the outputs to a provided `printer` function. The quiet mode prints
    a loading animation while the command is running and prints the output to
    a provided function.
    """

    def __init__(self, shell: str = SHELL, sudo: bool = False) -> None:
        """Create a new Shell object with the provided shell. If `sudo` is
        `True`, the user will be prompted for their password.

        Args:
            shell (str): The shell to use for commands execution.
            sudo (bool): Whether to get sudo privileges.
        """
        self.shell: str = shell
        """The shell to use for commands execution.
        """
        self._password: str
        """The password used to get sudo privileges.
        """

        # set the user's password if sudo is enabled
        if sudo:
            self._password = _password_prompt()

    def run(self, cmd: str, printer: Callable, error_printer: Callable,
            sudo: bool = False) -> int:
        """Runs a shell command and prints the output and errors using the
        provided `printer` and `error_printer` functions.

        The `printer` and `error_printer` functions should take a string as an
        argument.

        Args:
            cmd (str): The command to run.
            printer (function): The function used to print the output.
            error_printer (function): The function used to print errors.
            sudo (bool): Whether to run command with sudo privileges.

        Returns:
            The exit code of the command.
        """
        # get sudo privileges if sudo is enabled
        if sudo:
            if not self._password:
                self._password = _password_prompt()
            _set_sudo_privileges(self._password)

        process = subprocess.Popen(cmd, shell=True, executable=self.shell,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        _print_process_output(process, printer, error_printer)
        return process.returncode

    def run_quiet(self, cmd: str, printer: Callable,
                  loading_string: str = LOADING_STR, sudo: bool = False) -> int:
        """Runs a shell command and waits for it to complete. A loading
        animation is printed using `builtins.print` while the command is
        running. The output of the command is printed using the provided
        `printer` function. If `sudo` is `True`, a `display` object is
        required.

        Args:
            cmd (str): The command to run.
            printer (function, optional): The command outputs printer.
            loading_str (str): The loading string to print.
            sudo (bool): Whether to run command with sudo privileges.

        Returns:
            The exit code of the command.
        """
        # get sudo privileges if sudo is enabled
        if sudo:
            if not self._password:
                self._password = _password_prompt()
            _set_sudo_privileges(self._password)

        process = subprocess.Popen(cmd, shell=True, executable=self.shell,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)

        # show loading animation
        _loader(process.poll, loading_string)
        output = process.communicate()  # get the standard output and error

        # print the standard outputs and errors then return the exit code
        if output[0].decode().strip() != "":
            printer(cmd + "\n" + output[0].decode().strip())
        return process.returncode

    def __call__(self, cmd: str, printer: Callable = print,
                 loading_string: str = LOADING_STR) -> int:
        return self.run_quiet(cmd, printer, loading_string)


def interactive() -> None:
    """Runs the shell in interactive mode. No output is logged when running in
    this mode. The shell used is the default shell of the `Shell` class, of
    which an instance is created for this mode.
    """
    from .display import Display
    from .colors import (bright_red as red,
                         bright_green as green,
                         bright_blue as blue)

    display = Display(no_logging=True)
    shell_instance = Shell()
    print("Shell interface written in Python. Shell: " + shell_instance.shell)
    print(blue("Type 'exit' to stop.\n"))

    exit_code = 0
    while True:
        # print prompt based on the exit code of the previous command
        if exit_code != 0:
            print(red("> "), end="")
        else:
            print(green("> "), end="")
        # read a command and break if it is "exit"
        command = input()
        if command == "exit":
            break

        # run the command and print output
        exit_code = shell_instance.run(command, display.print, display.error)


def _loader(condition: Callable, loading_string: str) -> None:
    """Prints a loading animation until `condition` does not return `None`. The
    loading animation is printed using the provided `loading_string`.

    Args:
        condition (function): The function that returns `None` to stop.
        loading_string (str): The loading string to print.
    """
    import time
    time.sleep(0.05)  # wait for the process to start

    counter = 0
    while condition() is None:
        # print the loading string and animation
        print(loading_string + LOADING_ANIMATION[counter])
        # wait after printing the animation for 1 second
        time.sleep(1 / len(LOADING_ANIMATION))
        # clear the line and increment the counter
        print(_LINE_UP + _LINE_CLEAR + _LINE_UP)
        counter = (counter + 1) % len(LOADING_ANIMATION)


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


def _password_prompt(prompt: str = "Enter your password to continue: ") -> str:
    """Prompts the user for a password and returns it.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        The password entered by the user.
    """
    import getpass
    return getpass.getpass(prompt)


def _set_sudo_privileges(password: str) -> None:
    """Sets the sudo privileges for the current user.

    Args:
        password (str): The password of the user.
    """
    from os import system
    command = f'echo {password} | sudo -Svp ""'
    returncode = system(command)
    # check if the user entered the correct password
    if returncode != 0:
        raise PermissionError("Failed to get sudo privileges.")


def __getattr__(name):
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


if __name__ == "__main__":
    print("Running shell in interactive mode:\n")
    interactive()
