#!/usr/bin/env zsh

symlink_dotfile() {
  ln -sfv $(grealpath $1) "$HOME/.$1"
}

symlink() {
  ln -sfv $(grealpath $1) "$HOME/$1"
}


echo "Creating symlinks ..."

pushd ./dots
symlink_dotfile .zshrc
symlink_dotfile .aliases
symlink_dotfile .gitconfig
symlink_dotfile .gitignore_global
symlink_dotfile .gitmessage

# SSH
mkdir "$HOME/.ssh"
ln -sfv $(grealpath ssh-config) "$HOME/.ssh/config"
popd

# oh-my-zsh theme
ln -s ~/dotfiles/other/common.zsh-theme $HOME/.oh-my-zsh/themes

# colorls configuration
mkdir -p ~/.config/colorls
ln -s ~/.dotfiles/dark_colors.yaml ~./config/colorls/dark_colors.yaml
