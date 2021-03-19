#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

# prompt the user for confirmation, skip installation if needed
prompt() {
    echo -e "\a"
    echo "Would you like to install ${rbold}$1${clear}? [Y|n]"
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
    echo "${bold}Homebrew is not installed...${clear}"
    return 1
fi

# prompt the user to choose the casks to install

# Open-source code editor
brew install --cask visual-studio-code
# Unpacks archive files
prompt the-unarchiver
# Open-source BitTorrent client
prompt transmission
# Free and open-source media player
prompt iina
# Control windows and applications right from your trackpad
prompt swish
# Smooths scrolling and set mouse scroll directions independently
prompt mos
# Tool to control external monitor brightness & volume
prompt monitorcontrol

# Web browser
prompt google-chrome
# Application uninstaller
prompt appcleaner
# System monitor for the menu bar
prompt stats
# QuickLook plug-in that renders source code with syntax highlighting
prompt qlcolorcode

# fonts
brew tap homebrew/cask-fonts
prompt font-hack-nerd-font
prompt font-sf-pro
prompt font-sf-compact
prompt font-sf-mono
prompt font-new-york

brew cleanup
