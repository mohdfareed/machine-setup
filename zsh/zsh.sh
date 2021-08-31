#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up Zsh...${clear}"

zsh_dir=$(dirname $0)
source $zsh_dir/zshenv

brew install zsh
brew install zsh-syntax-highlighting
# install oh-my-zsh
sh -c "$(curl -fsSL https://git.io/JvzfK)" "" --unattended

# create directories
mkdir -p $ZDOTDIR # zsh dotfiles dir
mkdir -p $(dirname $ZSH_COMPDUMP)
mkdir -p $(dirname $HISTFILE)

# symlink files
ln -siv "$zsh_dir/zshenv" "$HOME/.zshenv"
ln -siv "$zsh_dir/zshrc" "$ZDOTDIR/.zshrc"
ln -siv "$zsh_dir/aliases" "$ZDOTDIR/aliases"
ln -siv "$zsh_dir/functions" "$ZDOTDIR/functions"
ln -siv "$zsh_dir/common/common.zsh-theme" "$ZSH/themes"

# holds optional environment variables
# sources by zshenv
touch $ZDOTDIR/env_vars

# remove last login time prompt
touch $HOME/.hushlogin
# delete old zshrc files
rm -rf $HOME/.zshrc
rm -rf $HOME/.zsh_sessions
rm -rf $HOME/.zsh_history
