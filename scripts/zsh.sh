#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up Zsh...${clear}"

# install oh-my-zsh
sh -c "$(curl -fsSL https://git.io/JvzfK)" "" --unattended

# create directories
mkdir -p "$XDG_CONFIG_HOME/zsh"
mkdir -p "$XDG_DATA_HOME/zsh"
mkdir -p "$XDG_CACHE_HOME/zsh"

# symlink files
ln -siv "$DOTFILES/dots/zshenv" "$HOME/.zshenv"
ln -siv "$DOTFILES/dots/zshrc" "$ZDOTDIR/.zshrc"
ln -siv "$DOTFILES/dots/aliases" "$ZDOTDIR/.aliases"

# link oh-my-zsh theme
if [[ ! -f $DOTFILES/resources/common/common.zsh-theme ]]; then
    git -C $DOTFILES submodule update --init
fi
ln -siv $DOTFILES/resources/common/common.zsh-theme $ZSH/themes

# remove last login time prompt
touch $HOME/.hushlogin
# delete old zshrc files
rm -rf $HOME/.zshrc
rm -rf $HOME/.zsh_sessions
rm -rf $HOME/.zsh_history
