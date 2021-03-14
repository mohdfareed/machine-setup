#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

tput clear
echo "${bold}Installing latest LTS Node version...${clear}"

# check if rbenv is installed
brew ls --version nvm > /dev/null
if [[ $? != 0 ]] ; then
    echo "${bold}nvm is not installed.${clear}"
    echo "${bold}Would you like to install it?${clear}"
    echo -e "\a"
    echo "Press RETURN to continue or any other key to abort"
    read -sk answer

    if [[ $answer != $'\n' ]] ; then
    return 1
    fi

    # check if brew is installed before installing nvm
    which brew > /dev/null
    if [[ $? != 0 ]] ; then
        echo "${bold}Homebrew is not installed...${clear}"
        return 1
    fi

    brew install nvm
fi

# get the latest version number of Ruby
version=$(nvm list-remote 2> /dev/null | tail -1)

# prompt the user for confirmation to install latest ruby version
echo "\nCurrent Node versions installed:"
nvm list
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
