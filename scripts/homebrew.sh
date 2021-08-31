#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'
gbold='\033[1;32m'

tput clear
echo "${bold}Installing Homebrew...${clear}"

# check for homebrew and install it if needed
which brew > /dev/null
if [[ $? != 0 ]] ; then
    /bin/bash -c "$(curl -fsSL https://git.io/JIY6g)"
else
    brew update
fi

# fix “zsh compinit: insecure directories” message
chmod -R go-w "$(brew --prefix)/share"

echo "${bold}Installing Homebrew formulae and casks...${clear}"

brew install exa
brew install mas
brew install youtube-dl
brew install ffmpeg
brew install atomicparsley

brew install --cask visual-studio-code
brew install --cask iina
brew install --cask the-unarchiver
brew install --cask transmission
brew install --cask openinterminal
brew install --cask monitorcontrol
brew install --cask swish
brew install --cask appcleaner
brew install --cask mos
brew install --cask telegram

brew tap homebrew/cask-fonts
brew install font-fira-code
brew install font-fira-code-nerd-font
brew install font-sf-pro
brew install font-sf-compact
brew install font-sf-mono
