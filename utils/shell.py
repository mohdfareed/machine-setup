#!/usr/bin/env python3
"""Shell module executing shell commands. The module provides a shell class
that can be used to run shell commands and retrieve their outputs and return
codes. Upon import, the module creates a global shell instance and asks the
user for their password. Individual commands can't display sudo prompts, so
the password is cached and reused for all commands that require sudo access.
If user input is required, the user must be prompted outside the shell command.
"""

import getpass
import subprocess
import typing

from rich import print
from rich.console import Console

LOADING_STR: str = "Loading..."
"""The default string to print while waiting for a command to complete. It is
followed by a loading animation.
"""

shell: "Shell"
"""The root shell instance."""


class Shell:
    """A shell instance."""

    def __init__(
        self,
        output_handler: typing.Callable = print,
        error_handler: typing.Callable = print,
        silent_output_handler: typing.Optional[typing.Callable] = None,
    ) -> None:
        self.output_handler = output_handler
        self.error_handler = error_handler
        self.silent_handler = silent_output_handler

    def _run(
        self, command, env=None, silent=False, safe=False, status=LOADING_STR
    ) -> typing.Union[tuple[str, int], int]:
        self.status = status

        # show loading animation while command is running in background
        console = Console()
        with console.status(f"[green]{status}[/]") as status:
            # use popen to retrieve outputs in real time
            process = subprocess.Popen(
                command,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=isinstance(command, str),
                text=True,
            )
            output, returncode = self.print_output(process, silent, status)

        # handle return code and/or output
        if not safe and returncode != 0:
            self.error_handler(output) if output else None
            raise subprocess.CalledProcessError(returncode, command, output)
        return (output, returncode) if silent else returncode

    def print_output(self, process, silent, status):
        output = ""
        # print output in real time
        for line in process.stdout:
            if not silent:
                status.stop()
                self.output_handler(line, end="")
                status.start()

            # update status and log if silent
            elif line.strip():  # ignore empty lines
                status.update(f"[green]{line.strip()}[/]")
                (
                    self.silent_handler(line.strip())
                    if self.silent_handler
                    else ...
                )
            output += line
        return output.strip(), process.wait()

    @typing.overload
    def __call__(
        self,
        command,
        env=...,
        silent: typing.Literal[False] = ...,
        safe=...,
        status=...,
    ) -> int: ...

    @typing.overload
    def __call__(
        self,
        command,
        env=...,
        silent: typing.Literal[True] = ...,
        safe=...,
        status=...,
    ) -> tuple[str, int]: ...

    def __call__(
        self, command, env=None, silent=False, safe=False, status=LOADING_STR
    ) -> typing.Union[int, tuple[str, int]]:
        return self._run(
            command, env=env, silent=silent, safe=safe, status=status
        )


shell = Shell()
try:  # check if the user has sudo privileges
    shell("sudo -n true &> /dev/null", silent=True)
except subprocess.CalledProcessError:
    # the user doesn't have sudo privileges, prompt for the password
    password = getpass.getpass("\033[32m Enter your password: \033[30m")
    shell(f"echo {password} | sudo -Sv", silent=True)
