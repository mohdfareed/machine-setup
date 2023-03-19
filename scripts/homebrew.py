from .lib.display import Display
from .lib.shell import *


def setup(display: Display = Display(no_logging=True)):
    display.header("Setting up Homebrew...")
    display("Installing Homebrew...")
    # run(["/bin/bash", "-c", "$(curl -fsSL https://git.io/JIY6g)"])
