#!/usr/bin/env zsh

source ./scripts/homebrew.sh
source ./scripts/symlinks.sh

# remove last login time prompt
touch $HOME/.hushlogin

echo "Sourcing .zshrc ..."
source "$HOME/.zshrc"
echo "Installation complete!"
