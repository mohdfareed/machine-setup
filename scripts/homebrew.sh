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

# Mac App Store command-line interface
brew install mas

# Open-source code editor
brew install --cask visual-studio-code
# Unpacks archive files
brew install --cask the-unarchiver
# Open-source BitTorrent client
brew install --cask transmission
# Free and open-source media player
brew install --cask iina
# Control windows and applications right from your trackpad
brew install --cask swish
# Smooths scrolling and set mouse scroll directions independently
brew install --cask mos
# Tool to control external monitor brightness & volume
brew install --cask monitor control

# # Web browser
# brew install --cask google-chrome
# # Application uninstaller
# brew install --cask appcleaner

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
