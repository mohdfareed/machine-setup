#!/usr/bin/env zsh

CLR='\033[0m'
BOLD='\033[1m'
RBOLD='\033[1;31m'

# prompt the user for confirmation, skip installation if needed
prompt() {
    echo "\nWould you like to install ${RBOLD}$(mas info $1 | \
    head -n 1)${CLR}? [Y|n]"
    read answer

    case $answer in
        [Nn]* ) ;;
        * ) mas install $1;;
    esac
}


tput clear
echo "${BOLD}Installing App Store applications...${CLR}"

# ask if the user is signed-in to continue
echo "${BOLD}You need to be signed-in to the App Store to continue.${CLR}"
echo
read -sk "?Press RETURN to continue or any other key to abort" answer

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
