#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Installing homebrew...${clear}"

# Check for homebrew and install it if needed
which brew > /dev/null
if [[ $? != 0 ]] ; then
    /bin/bash -c "$(curl -fsSL \
        https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew is already installed..."
    brew update
fi

brew cleanup

# fix “zsh compinit: insecure directories”
chmod -R go-w "$(brew --prefix)/share"
