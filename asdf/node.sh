#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up node.js...${clear}"

source $DOTFILES/dots/zshenv

# create needed directories
mkdir -p $(dirname $NPM_CONFIG_USERCONFIG)
mkdir -p $(dirname $NODE_REPL_HISTORY)
mkdir -p $NPM_CONFIG_CACHE

# installed latest node version and set it as default
asdf plugin add nodejs
asdf install nodejs latest > /dev/null
asdf global nodejs latest

asdf reshim
