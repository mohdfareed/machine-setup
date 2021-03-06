#!/usr/bin/env zsh

if ! git clone https://github.com/mohdfareed/Dotfiles.git ~/.dotfiles; then
  git --git-dir ~/.dotfiles pull
fi

touch ~/.hushlogin
ln -s ~/.dotfiles/.zshrc ~/.zshrc
ln -s ~/.dotfiles/.gitconfig ~/.gitconfig
ln -s ~/.dotfiles/.gitignore_global ~/.gitignore_global

if ! type "$brew" > /dev/null; then
  /bin/bash -c "$(curl -fsSL \
    https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
brew bundle --file ~/.dotfiles/Brewfile
