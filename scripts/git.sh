#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up git...${clear}"
source $DOTFILES/dots/zshenv

brew install git
brew install gpg
brew install pinentry-mac

# symlink git configuration files
mkdir -p $XDG_CONFIG_HOME/git
ln -siv "$DOTFILES/dots/gitconfig" "$XDG_CONFIG_HOME/git/config"
ln -siv "$DOTFILES/dots/gitignore" "$XDG_CONFIG_HOME/git/ignore"

# setup gpg key
echo "Passphrase: ${bold}WYy85#1X3dP#OlOS${clear}"

mkdir -pm 0700 $GNUPGHOME
echo "pinentry-program /usr/local/bin/pinentry-mac" >> $GNUPGHOME/gpg-agent.conf

gpg_dir=$DOTFILES/resources
gpg --import $gpg_dir/gpg-public.key > /dev/null
gpg --allow-secret-key-import --import $gpg_dir/gpg-private.key > /dev/null
gpg --import-ownertrust $gpg_dir/gpg-ownertrust > /dev/null
