#!/usr/bin/env zsh

dotfiles="$DEVELOPER/.dotfiles"
clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

tput clear
echo "${bold}Setting up Zsh...${clear}"

# install oh-my-zsh
ZSH="$DEVELOPER/zsh/oh-my-zsh" sh -c "$(curl -fsSL \
https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
"" --unattended

# symlink profile
ln -siv "$dotfiles/dots/zshenv" "$HOME/.zshenv"
ln -siv "$dotfiles/dots/zshrc" "$DEVELOPER/zsh/.zshrc"
ln -siv "$dotfiles/dots/aliases" "$DEVELOPER/zsh/aliases"

# link oh-my-zsh theme
if [[ ! -f $dotfiles/other/common/common.zsh-theme ]]; then
    git -C $dotfiles submodule update --init
fi
ln -siv $dotfiles/other/common/common.zsh-theme $ZSH/themes

# delete oh-my-zsh created zshrc file
rm $HOME/.zshrc
