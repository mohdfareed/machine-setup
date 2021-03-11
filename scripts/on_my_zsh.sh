#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

tput clear
echo "${bold}Setting up Oh My Zsh...${clear}"

ZSH="$HOME/.config/oh-my-zsh" sh -c "$(curl -fsSL \
https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
"" --unattended

# link oh-my-zsh theme
if [[ ! -f $HOME/.dotfiles/other/common/common.zsh-theme ]]; then
    git -C $HOME/.dotfiles submodule update --init
fi
ln -siv $HOME/.dotfiles/other/common/common.zsh-theme $ZSH/themes
