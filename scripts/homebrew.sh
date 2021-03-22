#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'
gbold='\033[1;32m'

# prompt the user for confirmation before installation
prompt() {
    echo -e "\a"
    echo "Would you like to install ${gbold}$1${clear}? [y|N]"
    read answer

    case $answer in
        [Yy]* )
            brew install $1 ;;
        * ) ;;
    esac
}

tput clear
echo "${bold}Installing homebrew...${clear}"

# Check for homebrew and install it if needed
which brew > /dev/null
if [[ $? != 0 ]] ; then
    /bin/bash -c "$(curl -fsSL https://git.io/JIY6g)"
else
    echo "Homebrew is already installed..."
    brew update
fi

# fix “zsh compinit: insecure directories” message
chmod -R go-w "$(brew --prefix)/share"

echo "${bold}Installing homebrew formulae and casks...${clear}"

## required formulae and casks

# UNIX shell (command interpreter)
brew install zsh
# Fish shell like syntax highlighting for zsh
brew install zsh-syntax-highlighting
# Distributed revision control system
brew install git
# Mac App Store command-line interface
brew install mas
# Open-source code editor
brew install visual-studio-code
# Free and open-source media player
brew install iina
# Unpacks archive files
brew install the-unarchiver
# Open-source BitTorrent client
brew install transmission
# Control windows and applications right from your trackpad
brew install swish
# Smooths scrolling and set mouse scroll directions independently
brew install mos
# Tool to control external monitor brightness & volume
brew install monitorcontrol

## Optional formulae and casks

# Modern replacement for 'ls'
prompt exa
# Play, record, convert, and stream audio and video
prompt ffmpeg # youtube-dl dependency
# Download YouTube videos from the command-line
prompt youtube-dl
# Web browser
prompt google-chrome
# Application uninstaller
prompt appcleaner
# System monitor for the menu bar
prompt stats
# QuickLook plug-in that renders source code with syntax highlighting
prompt qlcolorcode

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
