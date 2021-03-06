#!/usr/bin/env zsh

# remove last login time prompt
touch ~/.hushlogin

# symlink config files
ln -s ~/.dotfiles/.zshrc ~/.zshrc
ln -s ~/.dotfiles/.gitconfig ~/.gitconfig
ln -s ~/.dotfiles/.gitignore_global ~/.gitignore_global

# install homebrew if it is not already installed
if ! (( $+commands[brew] )); then
  /bin/bash -c "$(curl -fsSL \
    https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# UNIX shell (command interpreter)
brew install zsh
# Distributed revision control system
brew install git
# Interpreted, interactive, object-oriented programming language
brew install python

# Open-source code editor
brew install --cask visual-studio-code
# Unpacks archive files
cask the-unarchiver
# Open-source BitTorrent client
brew install --cask transmission
# Free and open-source media player
brew install --cask iina

# remove outdated formulae and casks
brew cleanup

# fix “zsh compinit: insecure directories”
chmod -R go-w "$(brew --prefix)/share"
