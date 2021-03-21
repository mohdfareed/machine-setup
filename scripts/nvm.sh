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
    echo "${rbold}Error:${clear}"
    echo "\tHomebrew is not installed..."
    return 1
fi

brew install nvm
brew cleanup

tput clear
echo "${bold}Installing latest Node version...${clear}"

if [[ ! -d $DOTFILES ]] ; then
    echo "${rbold}Error:${clear}"
    echo "\tDOTFILES directory does not exist..."
    return 1
fi

source $DOTFILES/dots/zshrc > /dev/null

# get the latest version number of nvm
version=$(nvm list-remote > /dev/null | tail -1)

# prompt the user for confirmation to install latest nvm version
echo -e "\a"
echo "Would you like to install Node ${gbold}$version${clear}? [Y|n]"
read answer

case $answer in
        [Nn]* )
            ;;
        * )
            # installed latest Node version and set it as default
            nvm install node
            ;;
esac
