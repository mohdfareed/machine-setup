#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

# prompt the user for confirmation, skip installation if needed
prompt() {
    echo -e "\a"
    echo "Would you like to install ${rbold}$(mas info $1 | \
        head -n 1)${clear}? [Y|n]"
    read answer

    case $answer in
        [Nn]* ) ;;
        * ) mas install $1;;
    esac
}


tput clear
echo "${bold}Installing App Store applications...${clear}"

# check if mas is installed before installing rbenv
which mas > /dev/null
if [[ $? != 0 ]] ; then
    echo "${bold}mas is not installed...${clear}"
else
    # ask if the user is signed-in to continue
    echo "${bold}You need to be signed-in to the App Store to continue.${clear}"
    echo -e "\a"
    echo "Press RETURN to continue or any other key to abort"
    read -sk answer

    # prompt the user to choose the apps to install
    if [[ $answer = $'\n' ]] ; then
        prompt 441258766  # Magnet
        prompt 409201541  # Pages
        prompt 409203825  # Numbers
        prompt 409183694  # Keynote
        prompt 1320666476 # Wipr
        prompt 1438243180 # Dark Reader
        prompt 1505779553 # Dashlane
        prompt 937984704  # Amphetamine
    fi
fi
