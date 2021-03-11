#!/usr/bin/env zsh

dotfiles="$HOME/.dotfiles/dots"
username="mohdfareed"
pat='3b82f82e9087eb0db848fada1b1f239ee43a46db' # personal access token


# clone dotfiles repo and its submodules
git clone https://$username:$pat@github.com/mohdfareed/dotfiles.git $dotfiles
git -C $dotfiles submodule update --init

# symlink git configuration files
ln -siv "$dotfiles/gitconfig" "$HOME/.gitconfig"
ln -siv "$dotfiles/gitignore_global" "$HOME/.gitignore_global"
