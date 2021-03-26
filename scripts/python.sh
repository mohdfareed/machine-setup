#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

tput clear
echo "${bold}Setting up python...${clear}"

# check if brew is installed
which brew > /dev/null
if [[ $? != 0 ]] ; then
    echo "${rbold}Error:${clear} Homebrew is not installed..."
    return 1
fi

brew install python
brew install pyenv
brew cleanup

if [[ ! -d $DOTFILES ]] ; then
    echo "${rbold}Error:${clear} DOTFILES directory does not exist..."
    return 1
fi

source $DOTFILES/dots/zshenv
source $DOTFILES/dots/zshrc > /dev/null

mkdir -p $XDG_CONFIG_HOME/python
ln -siv "$DOTFILES/dots/pythonrc" "$PYTHONSTARTUP"

# prompt the user to selected python version to install
echo -e "\a"
echo "Which python version would you like to install?"
echo
echo "${bold}Installed versions:${clear}"
pyenv versions
echo "${bold}Available versions:${clear}"
pyenv install -l 2> /dev/null
read version

# install selected Ruby version and set it as default
pyenv install $version
if [[ $? != 0 ]] ; then
    return 1
fi
pyenv global $version
pyenv rehash
eval "$(pyenv init -)" # update the current session's ruby
