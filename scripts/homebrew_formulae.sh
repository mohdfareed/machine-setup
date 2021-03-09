#!/usr/bin/env zsh

CLR='\033[0m'
BOLD='\033[1m'
RBOLD='\033[1;31m'

# prompt the user for confirmation, skip installation if needed
prompt() {
    echo "\nWould you like to install ${RBOLD}$1${CLR}? [Y|n]"
    read answer

    case $answer in
        [Nn]* ) ;;
        * ) brew install $1;;
    esac
}


tput clear
echo "${BOLD}Installing homebrew formulae...${CLR}"

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

brew cleanup
