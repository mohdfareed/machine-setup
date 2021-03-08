#!/usr/bin/env zsh

# prompt the user for confirmation
while true; do
    echo "You need to be signed-in to the App Store to continue."
    echo "Are you signed-in?[y|N]"
    read answer

    case $answer in
        [Yy]* )
            break;;
        * )
            exit;;
    esac
done

mas install 441258766 # Magnet
mas install 409201541 # Pages
mas install 409203825 # Numbers
mas install 409183694 # Keynote
mas install 1320666476 # Wipr
mas install 1438243180 # Dark Reader
mas install 1505779553 # Dashlane
