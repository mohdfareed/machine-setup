#!/usr/bin/env zsh

symlink_dotfile() {
  ln -sfv $1 "$HOME/.$1"
}


echo "Creating symlinks ..."

pushd ./dots
symlink_dotfile .zshrc
symlink_dotfile .aliases
symlink_dotfile .gitconfig
symlink_dotfile .gitignore_global

# oh-my-zsh theme
git -C ~/.dotfiles/other/common pull
ln -s ~/.dotfiles/other/common/common.zsh-theme $HOME/.oh-my-zsh/themes

# colorls configuration
mkdir -p ~/.config/colorls
ln -s ~/.dotfiles/other/dark_colors.yaml ~./config/colorls/dark_colors.yaml
