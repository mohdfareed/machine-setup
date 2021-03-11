#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

# prompt user for confirmation

tput clear
echo "${bold}Setting Terminal default settings. \
${rbold}Terminal app will be restarted...${clear}"
echo -e "\a"
read -sk "?Press RETURN to continue or any other key to abort" answer

# prompt the user to choose the apps to install
if [[ $answer != $'\n' ]] ; then
    exit
fi

# profile's path and name
pf_path=$(find $HOME/.dotfiles/other -maxdepth 1 -name "*.terminal" | head -n 1)
pf_name=$(basename $pf_path .terminal)

# add profile to terminal app
open $pf_path

# set profile as the default
defaults write com.apple.terminal "Default Window Settings" "$pf_name"
defaults write com.apple.terminal "Startup Window Settings" "$pf_name"
# show tabs bar
defaults write com.apple.terminal \
"NSWindowTabbingShoudShowTabBarKey-TTWindow-TTWindowController-\
TTWindowController-VT-FS" 1

echo "Restart Terminal for the changes to take effect."