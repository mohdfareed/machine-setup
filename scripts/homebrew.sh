#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

tput clear
echo "${bold}Installing homebrew ...${clear}"

# Check for homebrew and install it if needed
which -s brew
if [[ $? != 0 ]] ; then
    /bin/bash -c "$(curl -fsSL \
        https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew already installed ..."
    brew update
fi

brew cleanup

# fix “zsh compinit: insecure directories”
chmod -R go-w "$(brew --prefix)/share"
