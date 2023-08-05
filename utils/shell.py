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

    def _run(
        self, command, env=None, silent=False, safe=False, status=LOADING_STR
    ) -> typing.Union[tuple[str, int], int]:
        console = Console()

        # execute command while print loading status
        with console.status(f"[green]{status}[/]") as status:
            # use popen to print output in real time
            process = subprocess.Popen(
                command,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=isinstance(command, str),
                text=True,
            )

            # print output and wait for process to complete
            if not silent and process.stdout:
                status.stop()
                for line in process.stdout:
                    self.output_handler(line, end="")
            returncode = process.wait()

        # handle return code and/or output
        output = process.stdout.read().strip() if process.stdout else None
        if not safe and returncode != 0:
            self.error_handler(output) if output else None
            raise subprocess.CalledProcessError(returncode, command, output)
        return (output or "", returncode) if silent else returncode

    @typing.overload
    def __call__(
        self,
        command,
        env=...,
        silent: typing.Literal[False] = ...,
        safe=...,
        status=...,
    ) -> int:
        ...

    @typing.overload
    def __call__(
        self,
        command,
        env=...,
        silent: typing.Literal[True] = ...,
        safe=...,
        status=...,
    ) -> tuple[str, int]:
        ...

    def __call__(
        self, command, env=None, silent=False, safe=False, status=LOADING_STR
    ) -> typing.Union[int, tuple[str, int]]:
        return self._run(
            command, env=env, silent=silent, safe=safe, status=status
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
        exit_code = shell(cmd)


if __name__ == "__main__":
    print("[bold]Running shell in interactive mode.[/]\n")
    interactive()
