#!/usr/bin/env zsh

# remove last login time prompt
touch $HOME/.hushlogin

# update submodules
git -C $HOME/.dotfiles submodule update --init

source $HOME/.dotfiles/scripts/homebrew.sh
source $HOME/.dotfiles/scripts/symlink.sh

echo "Sourcing .zshrc ..."
source "$HOME/.zshrc"

source $HOME/.dotfiles/scripts/ruby.sh

open $HOME/.dotfiles/other/Personal.terminal
echo "'Personal' profile has been added to the terminal."
echo "Set it as the default through the Preferences."
echo "Installation complete!"
