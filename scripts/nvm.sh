#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'
gbold='\033[1;32m'

tput clear
echo "${bold}Setting up nvm...${clear}"

# check if brew is installed
which brew > /dev/null
if [[ $? != 0 ]] ; then
    echo "${rbold}Error:${clear} Homebrew is not installed..."
    return 1
fi

brew install nvm
brew cleanup

if [[ ! -d $DOTFILES ]] ; then
    echo "${rbold}Error:${clear} DOTFILES directory does not exist..."
    return 1
fi

source $DOTFILES/dots/zshenv
source $DOTFILES/dots/zshrc > /dev/null

# get the latest version number of nvm
version=$(nvm list-remote > /dev/null | tail -1)

# prompt the user for confirmation to install latest nvm version
echo -e "\a"
echo "Would you like to install Node ${gbold}$version${clear}? [Y|n]"
read answer

case $answer in
        [Nn]* )
            return 1
            ;;
        * )
            ;;
esac

# installed latest Node version and set it as default
nvm install node
nvm use node

# set npm cache folder and config file
npm config set cache $XDG_CACHE_HOME/npm --global
npm config set userconfig $XDG_CONFIG_HOME/npm/npmrc --global
