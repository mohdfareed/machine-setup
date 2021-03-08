#!/usr/bin/env zsh

echo "Installing homebrew ..."

# Check for homebrew and install if needed
which -s brew
if [[ $? != 0 ]] ; then
  /bin/bash -c "$(curl -fsSL \
    https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
  echo "Homebrew already installed ..."
fi

brew update

# UNIX shell (command interpreter)
brew install zsh
# Fish-like fast/unobtrusive autosuggestions for zsh
brew install zsh-autosuggestions
# Fish shell like syntax highlighting for zsh
brew install zsh-syntax-highlighting

# Distributed revision control system
brew install git
# Interpreted, interactive, object-oriented programming language
brew install python
# Ruby version manager
brew install rbenv

# Open-source code editor
brew install --cask visual-studio-code
# Unpacks archive files
brew install --cask the-unarchiver
# Open-source BitTorrent client
brew install --cask transmission
# Free and open-source media player
brew install --cask iina

# Mac App Store command-line interface
brew install mas
mas install 441258766 # Magnet
mas install 409201541 # Pages
mas install 409203825 # Numbers
mas install 409183694 # Keynote
mas install 1320666476 # Wipr
mas install 1438243180 # Dark Reader
mas install 1505779553 # Dashlane

# fonts
brew tap homebrew/cask-fonts
brew install --cask font-hack-nerd-font
brew install --cask font-sf-pro
brew install --cask font-sf-compact
brew install --cask font-sf-mono
brew install --cask font-new-york

brew cleanup

# fix “zsh compinit: insecure directories”
chmod -R go-w "$(brew --prefix)/share"
