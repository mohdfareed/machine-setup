#!/usr/bin/env zsh


# remove last login time prompt
touch $HOME/.hushlogin

# update submodules
git -C $HOME/.dotfiles submodule update --init

source $HOME/.dotfiles/scripts/homebrew.sh
source $HOME/.dotfiles/scripts/symlink.sh

echo "Sourcing .zshrc ..."
source "$HOME/.zshrc"

open $HOME/.dotfiles/other/Personal.terminal
echo "Set the added profile, 'Personal', as the default."
echo "Installation complete!"
