#!/usr/bin/env zsh

touch ~/.hushlogin
ln -s ~/.dotfiles/.zshrc ~/.zshrc
ln -s ~/.dotfiles/.gitconfig ~/.gitconfig
ln -s ~/.dotfiles/.gitignore_global ~/.gitignore_global

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
# GIT client
brew install --cask fork
# Unpacks archive files
cask the-unarchiver
# Open-source BitTorrent client
brew install --cask transmission
# Free and open-source media player
brew install --cask iina

brew cleanup
