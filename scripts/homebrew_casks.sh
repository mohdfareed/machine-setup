#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'
gbold='\033[1;32m'

# prompt the user for confirmation, skip installation if needed
prompt() {
    echo -e "\a"
    echo "Would you like to install ${gbold}$1${clear}? [Y|n]"
    read answer

    case $answer in
        [Nn]* ) ;;
        * ) brew install --cask $1;;
    esac
}


tput clear
echo "${bold}Installing homebrew casks...${clear}"

# check if brew is installed before installing rbenv
which brew > /dev/null
if [[ $? != 0 ]] ; then
    echo "${rbold}Error:${clear}"
    echo "\tHomebrew is not installed..."
    return 1
fi

## required casks

# Open-source code editor
brew install --cask visual-studio-code
# Free and open-source media player
brew install --cask iina
# Unpacks archive files
brew install --cask the-unarchiver
# Open-source BitTorrent client
brew install --cask transmission
# Control windows and applications right from your trackpad
brew install --cask swish
# Smooths scrolling and set mouse scroll directions independently
brew install --cask mos
# Tool to control external monitor brightness & volume
brew install --cask monitorcontrol

## prompt the user to choose the casks to install

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
brew install --cask font-sf-pro
brew install --cask font-sf-compact
brew install --cask font-sf-mono

# optional
prompt font-new-york
prompt font-hack-nerd-font

brew cleanup
