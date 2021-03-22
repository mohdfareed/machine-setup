#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up Zsh...${clear}"

if [[ ! -d $DOTFILES ]] ; then
    echo "${rbold}Error:${clear}"
    echo "\tDOTFILES directory does not exist..."
    return 1
fi

source $DOTFILES/dots/zshenv

# install oh-my-zsh
sh -c "$(curl -fsSL https://git.io/JvzfK)" "" --unattended

# symlink files
mkdir -p $ZDOTDIR
mkdir -p $(dirname $ZSH_COMPDUMP)
ln -siv "$DOTFILES/dots/zshenv" "$HOME/.zshenv"
ln -siv "$DOTFILES/dots/zshrc" "$ZDOTDIR/.zshrc"
ln -siv "$DOTFILES/dots/aliases" "$ZDOTDIR/.aliases"
ln -siv "$DOTFILES/dots/lazy_loader" "$ZDOTDIR/.lazy_loader"

# link oh-my-zsh theme
if [[ ! -f $DOTFILES/other/common/common.zsh-theme ]]; then
    git -C $DOTFILES submodule update --init
fi
ln -siv $DOTFILES/other/common/common.zsh-theme $ZSH/themes

source $ZDOTDIR/.zshrc

# delete old zshrc files
rm -rf $HOME/.zshrc
rm -rf $HOME/.zsh_sessions
rm -rf $HOME/.zsh_history
