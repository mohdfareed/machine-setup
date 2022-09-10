#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up git...${clear}"

git_dir=$(dirname "${0:a}")
source "$(dirname "$git_dir")/zsh/zshenv"

brew install git
brew install gpg
brew install pinentry-mac

# symlink git configuration files
mkdir -p "$XDG_CONFIG_HOME/git"
ln -sfv "$git_dir/gitconfig" "$XDG_CONFIG_HOME/git/config"
ln -sfv "$git_dir/gitignore" "$XDG_CONFIG_HOME/git/ignore"

# setup gpg key
mkdir -pm 0700 "$GNUPGHOME"
echo "pinentry-program /opt/homebrew/bin/pinentry-mac" >>"$GNUPGHOME/gpg-agent.conf"
echo "Passphrase: ${bold}AC#s!7cdSXXP6?hM${clear}"

# import keys and fix owner trust level

gpg --import "$git_dir/public.key" >/dev/null
gpg --import "$git_dir/private.key" >/dev/null

gpg --import "$git_dir/rit-public.key" >/dev/null
gpg --import "$git_dir/rit-private.key" >/dev/null

gpg --import-ownertrust "$git_dir/gpg-ownertrust" >/dev/null
