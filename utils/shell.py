"""Shell commands execution. The module provides a function that can be used
to run shell commands and retrieve their outputs and return codes.
Individual commands can't display sudo prompts, so the password is cached and
reused for all commands that require sudo access.
If user input is required, the user must be prompted outside the shell command.
"""

import logging
import subprocess

LOGGER = logging.getLogger(__name__)
"""The shell logger."""

_ERROR_TOKENS = ["error"]
_WARNING_TOKENS = ["warning"]
_SUDO_TOKEN = "sudo"


def run(command: str, env=None, throws=True, info=False) -> tuple[int, str]:
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
    if _SUDO_TOKEN in command.lower():
        LOGGER.debug("Running sudo command: %s", command)

    # execute the command
    with subprocess.Popen(
        command,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        text=True,
        executable="/bin/zsh",
    ) as process:
        (output, returncode) = _exec_process(process, info)

    # handle return code and/or output
    if throws and returncode != 0:
        raise ShellError(returncode, command, output)
    return returncode, output


def _exec_process(
    process: subprocess.Popen[str], info=False
) -> tuple[str, int]:

    output = ""  # if the process has no output
    if process.stdout is None:
        return output, process.wait()

    while True:  # read output from the process in real time
        line = process.stdout.readline().strip()
        _log_line(line, info)  # log the line
        output += line

        # break if process is done
        if process.poll() is not None:
            break
    return output.strip(), process.wait()


def _log_line(line: str, info: bool) -> None:
    if not line:
        return

    if any(token in line.lower() for token in _ERROR_TOKENS):
        LOGGER.error(line)
    elif any(token in line.lower() for token in _WARNING_TOKENS):
        LOGGER.warning(line)
    elif info:
        LOGGER.info(line)
    else:
        LOGGER.debug(line)


class ShellError(Exception):
    """Exception due to a shell error."""
