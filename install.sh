#!/usr/bin/env zsh

# remove last login time prompt
touch $HOME/.hushlogin

source ./scripts/homebrew.sh
sh -c "$(curl -fsSL \
  https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
source ./scripts/symlinks.sh

echo "Sourcing .zshrc ..."
source "$HOME/.zshrc"
echo "Installation complete!"
