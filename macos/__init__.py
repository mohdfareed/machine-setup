"""macOS-specific configuration files."""

import os as _os

# macos
macos = _os.path.dirname(_os.path.realpath(__file__))
"""The path of git configuration directory."""
brewfile = _os.path.join(macos, "brewfile")
"""The path of macOS specific Homebrew packages file."""
ps_profile = _os.path.join(macos, "powershell.ps1")
"""The path of the PowerShell profile file."""
preferences = _os.path.join(macos, "preferences.sh")
"""The path of macOS preferences file of shell commands."""
ssh_config = _os.path.join(macos, "ssh.config")
"""The path of the global ssh config file."""
zshenv = _os.path.join(macos, "zshenv")
"""The path of macOS zshenv file."""
zshrc = _os.path.join(macos, "zshrc")
"""The path of macOS zshrc file."""
