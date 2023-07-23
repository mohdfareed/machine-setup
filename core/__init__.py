"""Library of modules containing setup methods used for setting up a new
machine. These methods are imported and used by the main `setup.py` script. The
modules in this library depend on modules in the `utils` library.
"""

import os as _os

core = _os.path.dirname(_os.path.abspath(_os.path.expanduser(__file__)))
"""The path to the core directory."""
raspberrypi = _os.path.join(core, "raspberrypi")
"""The path of Raspberry Pi scripts."""
