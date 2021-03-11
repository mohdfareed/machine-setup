#!/usr/bin/env zsh

dotfiles="$HOME/.dotfiles"
username="mohdfareed" # github username
pat='3b82f82e9087eb0db848fada1b1f239ee43a46db' # github personal access token


# clone dotfiles repo and its submodules
git clone https://$username:$pat@github.com/mohdfareed/dotfiles.gi
git -C $dotfiles submodule update --init

# symlink git configuration files
ln -siv "$dotfiles/dots/gitconfig" "$HOME/.gitconfig"
ln -siv "$dotfiles/dots/gitignore_global" "$HOME/.gitignore_global"

source $dotfiles/scripts/setup.sh
