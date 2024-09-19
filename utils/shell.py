"""Shell commands execution. The module provides a function that can be used
to run shell commands and retrieve their outputs and return codes.
Individual commands can't display sudo prompts, so the password is cached and
reused for all commands that require sudo access. If user input is required,
the user must be prompted outside the shell command."""

__all__ = ["run", "ShellResults", "ShellError"]

import logging
import os
import re
import subprocess
from enum import StrEnum
from typing import Any, Optional

LOGGER = logging.getLogger(__name__)
"""The shell logger."""

# log matching tokens
_ERROR_TOKENS = ["error"]
_WARNING_TOKENS = ["warning"]
_SUDO_TOKEN = "sudo"

_IS_WINDOWS = os.name == (_ := "nt")  # whether the OS is Windows
_ANSI_ESCAPE = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")  # ANSI escape codes


class SupportedExecutables(StrEnum):
    """Supported shell executables."""

    ZSH = "/bin/zsh"
    PWSH_WIN = "pwsh.exe"
    WSL = "wsl"


EXECUTABLE: SupportedExecutables = (
    SupportedExecutables.ZSH
    if not _IS_WINDOWS
    else SupportedExecutables.PWSH_WIN
)
"""The shell executable to use."""


def run(
    command: str,
    env: Optional[dict[str, Any]] = None,
    throws: bool = True,
    info: bool = False,
) -> "ShellResults":
    """Run a shell command and return its output and return code.

    Args:
        command (str | list[str]): The command to run.
        env (dict[str, str], optional): The environment variables to set for
            the command. Defaults to None.
        throws (bool, optional): Whether to throw an error if the command has a
            non-zero return code. Defaults to True.
        info (bool, optional): Wether to log output as info or debug. Defaults
            to False, logging as debug.

    Returns:
        tuple[int, str]: The return code and output of the command.

    Raises:
        ShellError: If the command has a non-zero return
        code and `throws` is True.
        KeyboardInterrupt: If the command is interrupted by the user.
    """
    if _SUDO_TOKEN in command.lower() and not _IS_WINDOWS:
        LOGGER.debug("Running sudo command: %s", command)

    # execute the command
    with _create_process(command, env) as process:
        results = _exec_process(process, info)

    # handle return code and/or output
    if throws and results.returncode != 0:
        raise ShellError(
            command=command,
            results=results,
        )
    return results


def _create_process(
    command: str, env: Optional[dict[str, Any]] = None
) -> subprocess.Popen[str]:
    sub_proc = None

    if EXECUTABLE == SupportedExecutables.PWSH_WIN:
        sub_proc = subprocess.Popen(  # pylint: disable=consider-using-with
            [EXECUTABLE, "-Command", command],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

    elif EXECUTABLE == SupportedExecutables.WSL:
        sub_proc = subprocess.Popen(  # pylint: disable=consider-using-with
            [EXECUTABLE, "-e", "bash", "-c", f"'{command}'"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

    else:  # default to unix shell
        sub_proc = subprocess.Popen(  # pylint: disable=consider-using-with
            command,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            executable=EXECUTABLE,
            shell=True,
            text=True,
        )

    return sub_proc


def _exec_process(
    process: subprocess.Popen[str], info: bool = False
) -> "ShellResults":

    output = ""  # if the process has no output
    if process.stdout is None:
        return ShellResults(process.wait(), output)

    while True:  # read output from the process in real time
        line = process.stdout.readline().strip()
        _log_line(line, info)  # log the line
        output += line

        # break if process is done
        if process.poll() is not None:
            break
    return ShellResults(process.wait(), _ANSI_ESCAPE.sub("", output.strip()))


def _log_line(line: str, info: bool) -> None:
    if not line:
        return

    # Strip ANSI escape codes
    line = _ANSI_ESCAPE.sub("", line)

    if any(token in line.lower() for token in _ERROR_TOKENS):
        LOGGER.error(line)
    elif any(token in line.lower() for token in _WARNING_TOKENS):
        LOGGER.warning(line)
    elif info:
        LOGGER.info(line)
    else:
        LOGGER.debug(line)


class ShellResults(tuple[int, str]):
    """Shell command output."""

    def __new__(cls, returncode: int, output: str):
        return super().__new__(cls, (returncode, output))

    def __init__(self, returncode: int, output: str):
        self.returncode = returncode
        self.output = output

    def __str__(self):
        return f"[{self.returncode}] {self.output}"

    def _repr__(self):
        return (
            f"ShellOutput(returncode={self.returncode}, output={self.output})"
        )


class ShellError(Exception):
    """Exception due to a shell error."""

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)


if _IS_WINDOWS:
    run(
        "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned "
        "-Scope Process -Force"
    )
