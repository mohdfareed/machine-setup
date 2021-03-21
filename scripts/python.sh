#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

tput clear
echo "${bold}Setting up latest version of python...${clear}"

if [[ ! -d $DOTFILES ]] ; then
    echo "${rbold}Error:${clear}"
    echo "\tDOTFILES directory does not exist..."
    return 1
fi

brew install python
brew cleanup

source $DOTFILES/dots/zshenv

mkdir -p $XDG_CONFIG_HOME/python
ln -siv "$DOTFILES/dots/pythonrc" "$XDG_CONFIG_HOME/python/pythonrc"
