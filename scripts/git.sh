#!/usr/bin/env zsh

## REQUIREMENTS:
# brew

dotfiles="$HOME/.dotfiles"
clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

tput clear
echo "${bold}Setting up git...${clear}"

# Check for homebrew and setup if needed
which -s brew
if [[ $? != 0 ]] ; then
    echo "${bold}Homebrew is not installed.${clear}"
    echo "${bold}Would you like to install it?${clear}"
    echo -e "\a"
    read -sk "?Press RETURN to continue or any other key to abort" answer

    if [[ $answer != $'\n' ]] ; then
    exit;
    fi

    source $dotfiles/scripts/homebrew.sh
fi

brew install git

# symlink git configuration files
ln -siv "$dotfiles/dots/gitconfig" "$HOME/.gitconfig"
ln -siv "$dotfiles/dots/gitignore_global" "$HOME/.gitignore_global"
