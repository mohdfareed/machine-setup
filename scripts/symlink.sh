#!/usr/bin/env zsh

CLR='\033[0m'
BOLD='\033[1m'
RBOLD='\033[1;31m'

# symbolically link file to home directory as a hidden file
symlink() {
    ln -siv "$HOME/.dotfiles/dots/$1" "$HOME/.$1"
}


tput clear
echo "${BOLD}Creating symlinks ...${CLR}"

# symbolically link dot files
symlink zshrc
symlink aliases
symlink gitconfig
symlink gitignore_global

# set oh-my-zsh theme
git -C $HOME/.dotfiles/other/common pull
ln -siv $HOME/.dotfiles/other/common/common.zsh-theme $HOME/.oh-my-zsh/themes

# colorls configuration
mkdir -p $HOME/.config/colorls
ln -siv $HOME/.dotfiles/other/dark_colors.yaml \
    $HOME/.config/colorls/dark_colors.yaml

# load new zsh profile
echo "\n${BOLD}Sourcing .zshrc ...${CLR}"
source "$HOME/.zshrc"
