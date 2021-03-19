#!/usr/bin/env zsh

mkdir -p $XDG_CONFIG_HOME/python
ln -siv "$DOTFILES/dots/pythonrc" "$XDG_CONFIG_HOME/python/pythonrc"
