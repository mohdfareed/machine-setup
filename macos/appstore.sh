#!/usr/bin/env zsh

clear='\e[0m'
bold='\e[1m'
red='\e[31m'

tput clear
echo "${bold}Installing App Store applications${clear}"

brew install mas

# install apps
mas install 1487937127 # Craft Docs
mas install 441258766  # Magnet
mas install 1438243180 # Dark Reader
mas install 1320666476 # Wipr
mas install 937984704  # Amphetamine
mas install 517914548  # Dashlane
mas install 1554235898 # Peek
mas install 409201541  # Pages
mas install 409203825  # Numbers
mas install 409183694  # Keynote
mas install 497799835  # Xcode
