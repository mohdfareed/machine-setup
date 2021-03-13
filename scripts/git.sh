#!/usr/bin/env zsh

## REQUIREMENTS:
# XDG_CONFIG_HOME environment variable

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

tput clear
echo "${bold}Setting up git...${clear}"

# Check for homebrew and setup if needed
which git > /dev/null
if [[ $? != 0 ]] ; then
    echo "${bold}Git is not installed...${clear}"
    exit 1
fi

# symlink git configuration files
ln -siv "$DOTFILES/dots/gitconfig" "$XDG_CONFIG_HOME/git/config"
ln -siv "$DOTFILES/dots/gitignore_global" "$XDG_CONFIG_HOME/git/ignore_global"
