#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

# prompt user for confirmation

tput clear
echo "${bold}Setting up Terminal app...${clear}"

if [[ ! -d $DOTFILES ]] ; then
    echo "${rbold}Error:${clear}"
    echo "\tDOTFILES directory does not exist..."
    return 1
fi

source $DOTFILES/dots/zshenv

# profile's path and name
p_file=$(find $DOTFILES/other -maxdepth 1 -name "*.terminal" | \
    head -n 1)
p_name=$(basename $p_file .terminal)

# add profile to terminal app
open $p_file

# set profile as the default
defaults write com.apple.terminal "Default Window Settings" "$p_name"
defaults write com.apple.terminal "Startup Window Settings" "$p_name"
# hide line marks
defaults write com.apple.Terminal ShowLineMarks -int 0
# show tabs bar
defaults write com.apple.terminal \
"NSWindowTabbingShoudShowTabBarKey-TTWindow-TTWindowController-\
TTWindowController-VT-FS" 1

echo "Delete the manpage profile for manpages opened in new windows to use \
the default profile."
echo "Restart Terminal app for the changes to take effect."
