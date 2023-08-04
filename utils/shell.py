#!/usr/bin/env python3
"""Shell module executing shell commands. The module provides a `run` function
for running shell commands and `run_quiet` for running commands without
printing their output. The provides an interactive mode of the shell.
"""

import os
import subprocess
import typing

from rich import print
from rich.console import Console

import utils

LOADING_STR: str = "Loading..."
"""The default string to print while waiting for a command to complete. It is
followed by a loading animation.
"""


class Shell:
    """A shell instance."""

    def __init__(
        self,
        output_handler: typing.Callable = print,
        error_handler: typing.Callable = print,
    ) -> None:
        self.output_handler = output_handler
        self.error_handler = error_handler

    @typing.overload
    def run(
        self,
        command,
        silent=...,
        text: typing.Literal[True] = ...,
        status=...,
        safe=...,
    ) -> tuple[str, int]:
        ...

    @typing.overload
    def run(
        self,
        command,
        silent=...,
        text: typing.Literal[False] = ...,
        status=...,
        safe=...,
    ) -> int:
        ...

    @typing.overload
    def run(
        self,
        command,
        silent=...,
        text: bool = ...,
        status=...,
        safe=...,
    ) -> int:
        ...

    def run(
        self, command, silent=False, text=True, status=None, safe=False
    ) -> typing.Union[tuple[str, int], int]:
        console = Console()
        pipe = subprocess.PIPE if text or not silent else subprocess.DEVNULL
        err = subprocess.STDOUT

        # print loading status
        with console.status(f"[green]{status or LOADING_STR}[/]") as status:
            is_shell = isinstance(command, str)
            process = subprocess.Popen(
                command, shell=is_shell, stdout=pipe, stderr=err, text=True
            )

            # print output
            if not silent and process.stdout:
                status.stop()
                for line in process.stdout:
                    self.output_handler(line, end="")
            returncode = process.wait()

            output = None
            if text:  # return output
                output = process.stdout.read().strip()

        # check return code
        if output and not safe and returncode != 0:
            self.error_handler(output)
            raise subprocess.CalledProcessError(
                returncode, command, output if text else None
            )

        if output:
            return output, returncode
        return returncode

    @typing.overload
    def __call__(
        self,
        command,
        silent=...,
        text: typing.Literal[True] = ...,
        status=...,
        safe=...,
    ) -> tuple[str, int]:
        ...

    @typing.overload
    def __call__(
        self,
        command,
        silent=...,
        text: typing.Literal[False] = ...,
        status=...,
        safe=...,
    ) -> int:
        ...

    @typing.overload
    def __call__(
        self,
        command,
        silent=...,
        text: bool = ...,
        status=...,
        safe=...,
    ) -> int:
        ...

    def __call__(
        self, command, silent=False, text=True, status=None, safe=False
    ) -> typing.Union[int, tuple[str, int]]:
        return self.run(
            command, silent=silent, text=text, status=status, safe=safe
        )


def interactive() -> None:
    """Runs the shell in interactive mode. No output is logged when running in
    this mode. The shell used is the default shell of the module."""

    def print_prompt(exitcode: int):
        home = os.path.expanduser("~")
        path = "~/" + os.path.relpath(os.getcwd(), home)
        color = "green" if exitcode == 0 else "red"
        print(f"[bright_black]{path} [/][{color}]➜ [/]", end="")

    shell = Shell()
    active_shell: str = shell("echo $0", silent=True)[0]
    print(f"Shell interface written in Python. Active shell: {active_shell}")
    print("[bold blue]Type 'exit' to stop.[/]\n")

    exit_code = 0
    while True:
        # print prompt based on the exit code of the previous command
        print_prompt(exit_code)
        # read a command and break if it is "exit"
        if (cmd := input()) == "exit":
            print("[bold magenta]Exiting shell...[/]")
            break
        # run the command and print output
        exit_code: int = shell(cmd, text=False)


if __name__ == "__main__":
    print("[bold]Running shell in interactive mode.[/]\n")
    interactive()
