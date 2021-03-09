#!/usr/bin/env zsh

brew update

echo "Installing homebrew formulae..."

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

brew cleanup
