#!/usr/bin/env zsh

echo "Updating..."

# update submodules
git -C $HOME/.dotfiles submodule update --init

# update brew and its forumlae and casks
brew update
brew upgrade
brew cleanup

# update App Store apps
echo "Upgrading App Store apps..."
mas upgrade

# install latest ruby version
source $HOME/.dotfiles/scripts/ruby.sh

# update oh-my-zsh
omz update

echo "Updating complete!"
