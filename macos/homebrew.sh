#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Installing Homebrew...${clear}"

# install homebrew
/bin/bash -c "$(curl -fsSL https://git.io/JIY6g)"
# fix “zsh compinit: insecure directories” message
chmod -R go-w "$(brew --prefix)/share"

brew install exa
brew install youtube-dl
brew install ffmpeg
brew install atomicparsley

brew install --cask visual-studio-code
brew install --cask raycast
brew install --cask iina
brew install --cask the-unarchiver
brew install --cask transmission
brew install --cask openinterminal
brew install --cask sf-symbols

brew install --cask swish          # trackpad utility
brew install --cask monitorcontrol # external monitors controls
brew install --cask mos            # mouse smooth scroll utility
brew install --cask zoom           # zoom virtual meetings platform

brew tap homebrew/cask-fonts

brew install font-fira-code
brew install font-fira-code-nerd-font
brew install font-sf-pro
brew install font-sf-compact
brew install font-sf-mono
brew install font-computer-modern
