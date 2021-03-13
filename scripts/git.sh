#!/usr/bin/env zsh

## REQUIREMENTS:
# brew

dotfiles="$DEVELOPER/dotfiles"
clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

tput clear
echo "${bold}Setting up git...${clear}"

# Check for homebrew and setup if needed
which brew > /dev/null
if [[ $? != 0 ]] ; then
    echo "${bold}Homebrew is not installed.${clear}"
    echo "${bold}Would you like to install it?${clear}"
    echo -e "\a"
    echo "Press RETURN to continue or any other key to abort"
    read -sk answer

    if [[ $answer != $'\n' ]] ; then
    exit;
    fi

    source $dotfiles/scripts/homebrew.sh
fi

brew install git

# symlink git configuration files
ln -siv "$dotfiles/dots/gitconfig" "$DEVELOPER/git/config"
ln -siv "$dotfiles/dots/gitignore_global" "$DEVELOPER/git/ignore_global"
