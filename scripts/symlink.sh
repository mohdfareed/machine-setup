#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

# symbolically link a file to home directory as a hidden file
symlink() {
    ln -siv "$HOME/.dotfiles/dots/$1" "$HOME/.$1"
}


tput clear
echo "${bold}Creating symlinks ...${clear}"

# link dot files
symlink zshrc
symlink aliases
symlink gitconfig
symlink gitignore_global

# link oh-my-zsh theme
git -C $HOME/.dotfiles/other/common pull
ln -siv $HOME/.dotfiles/other/common/common.zsh-theme $HOME/.oh-my-zsh/themes

# link colorls configuration
ln -siv $HOME/.dotfiles/other/dark_colors.yaml \
$HOME/.config/colorls/dark_colors.yaml
