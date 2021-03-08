#!/usr/bin/env zsh

symlink() {
  ln -siv "$HOME/.dotfiles/dots/$1" "$HOME/.$1"
}


echo "Creating symlinks ..."

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
  ~/.config/colorls/dark_colors.yaml
