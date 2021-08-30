#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up asdf...${clear}"

source $DOTFILES/dots/zshenv
asdf_dir=$(dirname $0)

brew install asdf

# symlink asdf configuration file
mkdir -p $(dirname $ASDF_CONFIG_FILE)
ln -siv "$asdf_dir/asdfrc" "$ASDF_CONFIG_FILE"
