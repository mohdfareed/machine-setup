"""Machines module containing setup scripts for different machines."""

import logging
import os

import config
import utils

PAM_SUDO = "/etc/pam.d/sudo_local"
"""The path to the sudo PAM configuration file on macOS."""
PAM_SUDO_MODULE = "pam_tid.so"
"""The name of the PAM module to enable Touch ID for sudo."""
PAM_SUDO_CONTENT = f"""
auth       sufficient     {PAM_SUDO_MODULE}
"""
"""The content to add to the sudo PAM configuration file to enable Touch ID."""

LOGGER = logging.getLogger(__name__)
"""The machine setup logger. Used by all machines."""


def load_private_machine(private_machine: str) -> None:
    """Load private machine configuration."""
    LOGGER.info("Loading private machine configuration: %s", private_machine)

    env_filename = os.path.basename(config.private_env)
    private_env = os.path.join(private_machine, env_filename)
    try:  # symlink private environment
        utils.symlink(private_env, config.private_env)
    except FileNotFoundError:
        LOGGER.warning("Private environment not found.")

    keys_dirname = os.path.basename(config.ssh_keys)
    ssh_keys = os.path.join(private_machine, keys_dirname)
    try:  # symlink SSH keys
        utils.symlink(ssh_keys, config.ssh_keys)
    except FileNotFoundError:
        LOGGER.warning("SSH keys not found.")
