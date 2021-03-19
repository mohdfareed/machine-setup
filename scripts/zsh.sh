#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

tput clear
echo "${bold}Setting up Zsh...${clear}"

source $HOME/.zshenv

# install oh-my-zsh
sh -c "$(curl -fsSL https://git.io/JvzfK)" "" --unattended

# symlink files
ln -siv "$DOTFILES/dots/zshenv" "$HOME/.zshenv"
ln -siv "$DOTFILES/dots/zshrc" "$ZDOTDIR/.zshrc"
ln -siv "$DOTFILES/dots/aliases" "$ZDOTDIR/.aliases"

source $HOME/.zshenv
source $ZDOTDIR/.zshrc 2> /dev/null

# delete old zshrc files
rm -rf $HOME/.zshrc
rm -rf $HOME/.zsh_sessions
rm -rf $HOME/.zsh_history

# link oh-my-zsh theme
if [[ ! -f $DOTFILES/other/common/common.zsh-theme ]]; then
    git -C $DOTFILES submodule update --init
fi
ln -siv $DOTFILES/other/common/common.zsh-theme $ZSH/themes
