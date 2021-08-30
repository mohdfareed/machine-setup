#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up git...${clear}"
source $DOTFILES/dots/zshenv

# symlink git configuration files
mkdir -p $XDG_CONFIG_HOME/git
ln -siv "$DOTFILES/dots/gitconfig" "$XDG_CONFIG_HOME/git/config"
ln -siv "$DOTFILES/dots/gitignore" "$XDG_CONFIG_HOME/git/ignore"

# setup gpg key
mkdir -pm 0700 $GNUPGHOME
echo "pinentry-program /usr/local/bin/pinentry-mac" >> $GNUPGHOME/gpg-agent.conf

echo "Passphrase: ${bold}iJDKCS6qn59o${clear}"
gpg --import $DOTFILES/resources/gpg_private.key > /dev/null
echo "test" | gpg --clearsign > /dev/null
