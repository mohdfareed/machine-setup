#!/usr/bin/env python3
from scripts.lib import display
import scripts.git as git
import scripts.homebrew as homebrew
import scripts.macos as macos
import scripts.python as python
import scripts.zsh as zsh


def main():
    display.debug = True
    homebrew.setup()
    git.setup()
    zsh.setup()
    python.setup()
    macos.setup()


if __name__ == "__main__":
    main()
