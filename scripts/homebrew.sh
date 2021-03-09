#!/usr/bin/env zsh

CLR='\033[0m'
BOLD='\033[1m'
RBOLD='\033[1;31m'

tput clear
echo "${BOLD}Installing homebrew ...${CLR}"

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
