#!/usr/bin/env zsh

## REQUIREMENTS:
# brew

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
        * ) brew install $1;;
    esac
}


tput clear
echo "${bold}Installing homebrew formulae...${clear}"

brew update

# prompt the user to choose the formulae to install

# UNIX shell (command interpreter)
prompt zsh
# Fish-like fast/unobtrusive autosuggestions for zsh
prompt zsh-autosuggestions
# Fish shell like syntax highlighting for zsh
prompt zsh-syntax-highlighting

# Distributed revision control system
prompt git
# Interpreted, interactive, object-oriented programming language
prompt python
# Ruby version manager
prompt rbenv

# Mac App Store command-line interface
prompt mas
# Play, record, convert, and stream audio and video
prompt ffmpeg # youtube-dl dependency
# Download YouTube videos from the command-line
prompt youtube-dl

brew cleanup
