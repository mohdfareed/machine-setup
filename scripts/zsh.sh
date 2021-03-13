#!/usr/bin/env zsh

DEVELOPER="$HOME/Developer"
DOTFILES="$DEVELOPER/dotfiles"
clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

tput clear
echo "${bold}Setting up Zsh...${clear}"

# install oh-my-zsh
ZSH="$DEVELOPER/zsh/oh-my-zsh" sh -c "$(curl -fsSL \
https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
"" --unattended

# symlink files
ln -siv "$DOTFILES/dots/zshenv" "$HOME/.zshenv"
ln -siv "$DOTFILES/dots/zshrc" "$DEVELOPER/zsh/.zshrc"
ln -siv "$DOTFILES/dots/aliases" "$DEVELOPER/zsh/.aliases"

# link oh-my-zsh theme
if [[ ! -f $DOTFILES/other/common/common.zsh-theme ]]; then
    git -C $DOTFILES submodule update --init
fi
ln -siv $DOTFILES/other/common/common.zsh-theme $ZSH/themes

# delete old zshrc files
rm -rf $HOME/.zshrc
rm -rf $HOME/.zsh_sessions
rm -rf $HOME/.zsh_history

source $HOME/.zshenv
source $DEVELOPER/zsh/.zshrc 2> /dev/null
