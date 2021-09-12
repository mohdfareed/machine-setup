#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up node.js...${clear}"

node_dir=$(dirname "$0")
source "$(dirname "$node_dir")/zsh/zshenv"

# create needed directories
mkdir -p "$(dirname "$NPM_CONFIG_USERCONFIG")"
mkdir -p "$(dirname "$NODE_REPL_HISTORY")"
mkdir -p "$NPM_CONFIG_CACHE"

# installed latest node version and set it as default
asdf plugin add nodejs
asdf install nodejs latest > /dev/null
asdf global nodejs latest
asdf reshim

# add environment variables
cat "$node_dir/env_vars" >> "$ZDOTDIR/env_vars"
echo >> "$ZDOTDIR/env_vars"
