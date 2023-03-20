"""Library of modules containing setup methods used for setting up a new
machine. These methods are imported and used by the `setup.py` script.
"""

from .homebrew import setup as setup_homebrew
from .macos import setup as setup_macos
from .git import setup as setup_git
from .python import setup as setup_python
from .zsh import setup as setup_zsh
