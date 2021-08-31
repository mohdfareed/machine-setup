#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up git...${clear}"

git_dir=$(dirname $0)
source $(dirname $git_dir)/zsh/zshenv

brew install git
brew install gpg
brew install pinentry-mac

# symlink git configuration files
mkdir -p $XDG_CONFIG_HOME/git
ln -siv "$git_dir/gitconfig" "$XDG_CONFIG_HOME/git/config"
ln -siv "$git_dir/gitignore" "$XDG_CONFIG_HOME/git/ignore"

# setup gpg key
mkdir -pm 0700 $GNUPGHOME
echo "pinentry-program /usr/local/bin/pinentry-mac" >> $GNUPGHOME/gpg-agent.conf
echo "Passphrase: ${bold}WYy85#1X3dP#OlOS${clear}"
# import key and fix owner trust level
gpg --import $git_dir/gpg-public.key > /dev/null
gpg --allow-secret-key-import --import $git_dir/gpg-private.key > /dev/null
gpg --import-ownertrust $git_dir/gpg-ownertrust > /dev/null
