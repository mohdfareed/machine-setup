"""Shell module executing shell commands. The module provides a shell class
that can be used to run shell commands and retrieve their outputs and return
codes. Upon import, the module creates a global shell instance and asks the
user for their password. Individual commands can't display sudo prompts, so
the password is cached and reused for all commands that require sudo access.
If user input is required, the user must be prompted outside the shell command.
"""

import getpass
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
        env (dict[str, str], optional): The environment variables to set for the
            command. Defaults to None.
        throws (bool, optional): Whether to throw an error if the command has a
            non-zero return code. Defaults to True.
        msg (str, optional): The status message to display while the command
            is running. Defaults to LOADING_STR.

    Returns:
        tuple[int, str]: The return code and output of the command.

    Raises:
        subprocess.CalledProcessError: If the command has a non-zero return code
            and `throws` is True.
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
        output, returncode = print_output(process, status, msg)
    # handle return code and/or output
    if throws and returncode != 0:
        raise subprocess.CalledProcessError(returncode, command, output)
    return returncode, output


def print_output(process, status, msg):
    output = ""
    while True:
        reads = [process.stdout.fileno(), process.stderr.fileno()]
        ret = select.select(reads, [], [])

        for fd in ret[0]:
            status.stop()
            if fd == process.stdout.fileno():
                line = process.stdout.readline()
                LOGGER.debug(line.strip()) if line.strip() else None
            if fd == process.stderr.fileno():
                line = process.stderr.readline()
                LOGGER.error(line.strip()) if line.strip() else None
            status.start()

            if line.strip():  # sanitize output and update status
                # limit line length due to status moving up if multiple lines
                last_line = line.strip()[:50]
                status.update(f"[green]{msg} | {last_line}...[/]")
            output += line

        if process.poll() is not None:
            break
    return output.strip(), process.wait()


def setup_sudo() -> None:
    """Setup sudo access for the current user."""
    try:  # check if the user has sudo privileges
        run("sudo -n true &> /dev/null")
    except subprocess.CalledProcessError:
        # the user doesn't have sudo privileges, prompt for the password
        while True:
            password = getpass.getpass(
                "\033[32m Enter your password: \033[30m"
            )
            cmd = f"echo {password} | sudo -Sv &> /dev/null"
            if run(cmd, throws=False)[0] == 0:
                break
            print("\033[31m Invalid password\033[30m")
