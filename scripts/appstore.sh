#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'
gbold='\033[1;32m'

# prompt the user for confirmation, skip installation if needed
prompt() {
    echo -e "\a"
    app_name=$(mas info $1 | head -n 1)
    echo "Would you like to install ${gbold}$app_name${clear}? [Y|n]"
    read answer

    case $answer in
        [Nn]* ) ;;
        * ) mas install $1;;
    esac
}


tput clear
echo "${bold}Installing App Store applications...${clear}"
echo -e "\a"
echo "Press RETURN to continue or any other key to abort"
read -sk answer
if [[ $answer != $'\n' ]] ; then
    return 0
fi

# check if mas is installed
which mas > /dev/null
if [[ $? != 0 ]] ; then
    echo "${rbold}Error:${clear} mas is not installed..."
    return 1
fi

# check if the user is signed-in to the App Store
mas account > /dev/null
if [[ $? != 0 ]] ; then
    echo "${rbold}Error:${clear} You need to be signed-in to the App Store..."
    return 1
fi

# install apps
mas install 441258766  # Magnet
mas install 1438243180 # Dark Reader
mas install 1320666476 # Wipr
mas install 1564688210 # Glance
mas install 937984704  # Amphetamine

# prompt the user install optional apps
prompt 1505779553 # Dashlane
prompt 409201541  # Pages
prompt 409203825  # Numbers
prompt 409183694  # Keynote
prompt 497799835  # Xcode
