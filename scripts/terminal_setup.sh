#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

# prompt user for confirmation

tput clear
echo "${bold}Setting up Terminal app...${clear}"

# profile's path and name
p_path=$(find $DOTFILES/other -maxdepth 1 -name "*.terminal" | \
head -n 1)
p_name=$(basename $pf_path .terminal)

# add profile to terminal app
open $p_path

# set profile as the default
defaults write com.apple.terminal "Default Window Settings" "$p_name"
defaults write com.apple.terminal "Startup Window Settings" "$p_name"
# show tabs bar
defaults write com.apple.terminal \
"NSWindowTabbingShoudShowTabBarKey-TTWindow-TTWindowController-\
TTWindowController-VT-FS" 1

echo "Restart Terminal for the changes to take effect."
