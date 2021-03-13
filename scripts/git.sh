#!/usr/bin/env zsh

## REQUIREMENTS:
# XDG_CONFIG_HOME environment variable

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

tput clear
echo "${bold}Setting up git configuration...${clear}"

# symlink git configuration files
mkdir -p $XDG_CONFIG_HOME/git
ln -siv "$DOTFILES/dots/gitconfig" "$XDG_CONFIG_HOME/git/config"
ln -siv "$DOTFILES/dots/gitignore_global" "$XDG_CONFIG_HOME/git/ignore_global"
