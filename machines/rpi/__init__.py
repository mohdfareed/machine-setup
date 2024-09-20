"""Raspberry Pi specific setup module."""

import os as _os

config = _os.path.join(_os.path.dirname(_os.path.realpath(__file__)), "config")
ssh_config = _os.path.join(config, "ssh.config")
zshenv = _os.path.join(config, "zshenv")
zshrc = _os.path.join(config, "zshrc")
