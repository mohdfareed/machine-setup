#!/usr/bin/env zsh

symlink_dotfile() {
  ln -sfv $1 "$HOME/.$1"
}


echo "Creating symlinks ..."

pushd $HOME/.dotfiles/dots
symlink_dotfile zshrc
symlink_dotfile aliases
symlink_dotfile gitconfig
symlink_dotfile gitignore_global

# oh-my-zsh theme
git -C $HOME/.dotfiles/other/common pull
ln -s $HOME/.dotfiles/other/common/common.zsh-theme $HOME/.oh-my-zsh/themes

# colorls configuration
mkdir -p $HOME/.config/colorls
ln -s $HOME/.dotfiles/other/dark_colors.yaml ~/.config/colorls/dark_colors.yaml
