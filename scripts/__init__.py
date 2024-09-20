"""Library of modules containing setup methods used for setting up a new
machine. These methods are imported and used by the main `setup.py` script. The
modules in this library depend on modules in the `utils` library."""

from . import git  # type: ignore
from . import package_managers  # type: ignore
from . import shell  # type: ignore
from . import ssh  # type: ignore
from . import tailscale  # type: ignore
from . import tools  # type: ignore
from . import vscode  # type: ignore
from .package_managers import *
from .tools import *
