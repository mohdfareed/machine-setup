#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'
gbold='\033[1;32m'

# prompt the user for confirmation before installation
prompt() {
    echo -e "\a"
    echo "Would you like to install ${gbold}${@: -1}${clear}? [y|N]"
    read answer

    case $answer in
        [Yy]* )
            brew install $@ ;;
        * ) ;;
    esac
}

tput clear
echo "${bold}Installing Homebrew...${clear}"

# check for homebrew and install it if needed
which brew > /dev/null
if [[ $? != 0 ]] ; then
    /bin/bash -c "$(curl -fsSL https://git.io/JIY6g)"
else
    echo "Homebrew is already installed..."
    brew update
fi

# fix “zsh compinit: insecure directories” message
chmod -R go-w "$(brew --prefix)/share"

echo "${bold}Installing Homebrew formulae and casks...${clear}"

## required formulae and casks

# UNIX shell (command interpreter)
brew install zsh
# Fish shell like syntax highlighting for zsh
brew install zsh-syntax-highlighting
# Distributed revision control system
brew install git
# Open-source code editor
brew install --cask visual-studio-code
# Free and open-source media player
brew install --cask iina
# File archiver
brew install --cask keka
brew install --cask kekaexternalhelper
# Open-source BitTorrent client
brew install --cask transmission

## Optional formulae and casks

# Mac App Store command-line interface
prompt mas
# Modern replacement for 'ls'
prompt exa
# Play, record, convert, and stream audio and video
prompt ffmpeg # youtube-dl dependency
# Download YouTube videos from the command-line
prompt youtube-dl
# Control windows and applications right from your trackpad
prompt --cask swish
# Smooths scrolling and set mouse scroll directions independently
prompt --cask mos
# Tool to control external monitor brightness & volume
prompt --cask monitorcontrol
# GIT client
prompt --cask fork
# Web browser
prompt --cask google-chrome
# Application uninstaller
prompt --cask appcleaner
# System monitor for the menu bar
prompt --cask stats
# QuickLook plug-in that renders source code with syntax highlighting
prompt --cask qlcolorcode

## fonts

brew tap homebrew/cask-fonts
# required
brew install font-sf-pro
brew install font-sf-compact
brew install font-sf-mono
# optional
prompt font-new-york
prompt font-hack-nerd-font

brew cleanup
