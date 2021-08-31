#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up Zsh...${clear}"

source $DOTFILES/dots/zshenv
zsh_dir=$(dirname $0)

brew install zsh
brew install zsh-syntax-highlighting

# install oh-my-zsh
sh -c "$(curl -fsSL https://git.io/JvzfK)" "" --unattended

# create directories
mkdir -p $ZDOTDIR
mkdir -p $(dirname $ZSH_COMPDUMP)
mkdir -p $(dirname $HISTFILE)

# symlink files
ln -siv "$zsh_dir/zshenv" "$HOME/.zshenv"
ln -siv "$zsh_dir/zshrc" "$ZDOTDIR/.zshrc"
ln -siv "$zsh_dir/aliases" "$ZDOTDIR/aliases"
ln -siv "$zsh_dir/functions" "$ZDOTDIR/functions"

# link oh-my-zsh theme
if [[ ! -f $zsh_dir/common/common.zsh-theme ]]; then
    git -C $DOTFILES submodule update --init
fi
ln -siv $zsh_dir/common/common.zsh-theme $ZSH/themes

# remove last login time prompt
touch $HOME/.hushlogin
# delete old zshrc files
rm -rf $HOME/.zshrc
rm -rf $HOME/.zsh_sessions
rm -rf $HOME/.zsh_history
