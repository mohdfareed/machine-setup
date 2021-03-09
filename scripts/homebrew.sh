#!/usr/bin/env zsh

echo "Installing homebrew ..."

# Check for homebrew and install if needed
which -s brew
if [[ $? != 0 ]] ; then
    /bin/bash -c "$(curl -fsSL \
        https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew already installed ..."
    
    brew update
    brew cleanup
fi

# fix “zsh compinit: insecure directories”
chmod -R go-w "$(brew --prefix)/share"
