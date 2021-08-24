#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up git...${clear}"
source $DOTFILES/dots/zshenv

# symlink git configuration files
mkdir -p $XDG_CONFIG_HOME/git
ln -siv "$DOTFILES/dots/gitconfig" "$XDG_CONFIG_HOME/git/config"
ln -siv "$DOTFILES/dots/gitignore" "$XDG_CONFIG_HOME/git/ignore"
