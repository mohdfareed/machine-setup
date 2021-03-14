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
        * ) brew install $1;;
    esac
}


tput clear
echo "${bold}Installing homebrew formulae...${clear}"

# check if brew is installed before installing rbenv
which brew > /dev/null
if [[ $? != 0 ]] ; then
    echo "${bold}Homebrew is not installed.${clear}"
else
    brew update

    # essential formulae

    # UNIX shell (command interpreter)
    brew install zsh
    # Fish shell like syntax highlighting for zsh
    brew install zsh-syntax-highlighting
    # Distributed revision control system
    brew install git

    # prompt the user to choose the formulae to install

    # Interpreted, interactive, object-oriented programming language
    prompt python
    # Ruby version manager
    prompt rbenv
    # Node version management
    prompt n

    # Mac App Store command-line interface
    prompt mas
    # Play, record, convert, and stream audio and video
    prompt ffmpeg # youtube-dl dependency
    # Download YouTube videos from the command-line
    prompt youtube-dl

    brew cleanup
fi
