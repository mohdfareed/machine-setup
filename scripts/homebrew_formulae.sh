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
    return 1
fi

# essential formulae
# install without prompting for confirmation

# UNIX shell (command interpreter)
brew install zsh
# Fish shell like syntax highlighting for zsh
brew install zsh-syntax-highlighting
# Distributed revision control system
brew install git

# development

# Interpreted, interactive, object-oriented programming language
prompt python
# Ruby version manager
prompt rbenv
# Node version management
prompt nvm

# Markdown Preview Enhanced vscode extension

# Graph visualization software. Used to display graphs in markdown preview
prompt graphviz
# Development kit for the Java programming language
# Used to display graphs in markdown preview
prompt java
# check if java is installed
brew list java > /dev/null
if [[ $? = 0 ]] ; then
    sudo ln -sfn $(brew --prefix)/opt/openjdk/libexec/openjdk.jdk \
        /Library/Java/JavaVirtualMachines/openjdk.jdk
fi

# utilities

# Mac App Store command-line interface
prompt mas
# Play, record, convert, and stream audio and video
prompt ffmpeg # youtube-dl dependency
# Download YouTube videos from the command-line
prompt youtube-dl

brew cleanup
