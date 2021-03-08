#!/usr/bin/env zsh

# remove last login time prompt
touch $HOME/.hushlogin

source $HOME/.dotfiles/scripts/homebrew.sh
sh -c "$(curl -fsSL \
  https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
source $HOME/.dotfiles/scripts/symlink.sh

echo "Sourcing .zshrc ..."
source "$HOME/.zshrc"
echo "Installation complete!"
