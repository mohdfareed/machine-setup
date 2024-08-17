"""Shell module executing shell commands. The module provides a shell class
that can be used to run shell commands and retrieve their outputs and return
codes. Upon import, the module creates a global shell instance and asks the
user for their password. Individual commands can't display sudo prompts, so
the password is cached and reused for all commands that require sudo access.
If user input is required, the user must be prompted outside the shell command.
"""

import logging
import select
import subprocess

from rich.console import Console

LOADING_STR: str = "Loading"
"""The default string to print while waiting for a command to complete. It is
followed by a loading animation."""
LOGGER = logging.getLogger(__name__)
"""The shell logger."""


def run(command, env=None, throws=True, msg=LOADING_STR) -> tuple[int, str]:
    """Run a shell command and return its output and return code.

    Args:
        command (str | list[str]): The command to run.
        env (dict[str, str], optional): The environment variables to set for
            the command. Defaults to None.
        throws (bool, optional): Whether to throw an error if the command has a
            non-zero return code. Defaults to True.
        msg (str, optional): The status message to display while the command
            is running. Defaults to LOADING_STR.

    Returns:
        tuple[int, str]: The return code and output of the command.

    Raises:
        subprocess.CalledProcessError: If the command has a non-zero return
        code and `throws` is True.
    """

    # show loading animation while command is running in background
    console = Console()
    with console.status(f"[green]{msg}[/]") as status:
        # use popen to retrieve outputs in real time
        process = subprocess.Popen(
            command,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=isinstance(command, str),
            text=True,
        )
        output, returncode = _print_output(process, status, msg)
    # handle return code and/or output
    if throws and returncode != 0:
        raise subprocess.CalledProcessError(returncode, command, output)
    return returncode, output


def _print_output(process, status, msg):
    output = ""
    while True:
        reads = [process.stdout.fileno(), process.stderr.fileno()]
        ret = select.select(reads, [], [])

        for fd in ret[0]:
            status.stop()
            line = ""
            if fd == process.stdout.fileno():
                if line := process.stdout.readline().strip():
                    LOGGER.debug(line)
            if fd == process.stderr.fileno():
                if line := process.stderr.readline().strip():
                    LOGGER.error(line)
            status.start()

            if line:  # sanitize output and update status
                # limit line length due to status moving up if multiple lines
                last_line = line[:50]
                status.update(f"[green]{msg} |[/] {last_line}...")
            else:  # update status with loading animation
                status.update(f"[green]{msg}[/]")
            output += line

        if process.poll() is not None:
            break
    return output.strip(), process.wait()
