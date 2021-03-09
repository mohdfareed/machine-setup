#!/usr/bin/env zsh

brew update

echo "Installing homebrew casks..."

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
