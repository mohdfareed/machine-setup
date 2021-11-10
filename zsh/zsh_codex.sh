#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up Zsh...${clear}"

zsh_dir=$(dirname "${0:a}")
source "$zsh_dir/zshenv"

pip install openai
git clone https://github.com/tom-doerr/zsh_codex.git $ZSH_CUSTOM/plugins/zsh_codex/
ln -sfv "$zsh_dir/openaiapirc" "$XDG_CONFIG_HOME/openaiapirc"
