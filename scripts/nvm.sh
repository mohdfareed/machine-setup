#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

tput clear
echo "${bold}Installing nvm and latest Node version...${clear}"

# check if brew is installed before installing nvm
which brew > /dev/null
if [[ $? != 0 ]] ; then
    echo "${bold}Homebrew is not installed...${clear}"
    return 1
fi

brew install nvm

# get the latest version number of nvm
version=$(nvm list-remote 2> /dev/null | tail -1)

# prompt the user for confirmation to install latest nvm version
echo -e "\a"
echo "Would you like to install Node ${rbold}$version${clear}? [Y|n]"
read answer

case $answer in
        [Yy]* )
            ;;
        * )
            # installed latest Node version and set it as default
            nvm install node
            ;;
esac
