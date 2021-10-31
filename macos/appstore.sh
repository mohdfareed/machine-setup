#!/usr/bin/env zsh

clear='\e[0m'
bold='\e[1m'
red='\e[31m'

tput clear
echo "${bold}Installing App Store applications${clear}"

brew install mas
# check if the user is signed-in to the App Store
mas account >/dev/null
if [[ $? != 0 ]]; then
    echo "${red}Error:${clear} You need to be signed-in to the App Store"
    return 1
fi

# install apps
mas install 441258766  # Magnet
mas install 1438243180 # Dark Reader
mas install 1320666476 # Wipr
mas install 937984704  # Amphetamine
mas install 517914548  # Dashlane
mas install 497799835  # Xcode
mas install 409201541  # Pages
mas install 409203825  # Numbers
mas install 409183694  # Keynote
mas install 1519213509 # iPreview
mas install 1487937127 # Craft Docs
