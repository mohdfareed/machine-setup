#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up asdf...${clear}"

asdf_dir=$(dirname "${0:a}")
source "$(dirname "$asdf_dir")/zsh/zshenv"

brew install asdf

# symlink asdf configuration file
mkdir -p "$(dirname "$ASDF_CONFIG_FILE")"
ln -sfv "$asdf_dir/asdfrc" "$ASDF_CONFIG_FILE"
