#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up git...${clear}"

# path to git scripts directory
git_dir=$(dirname "${0:a}")
# load zsh environment variables
source "$(dirname "$git_dir")/zsh/zshenv"

# install required packages
brew install git          # main git installation of the system
brew install gpg          # gpg package for signing commits
brew install pinentry-mac # pinentry for gpg

# symlink git configuration files
mkdir -p "$XDG_CONFIG_HOME/git" # create git config directory
ln -sfv "$git_dir/gitconfig" "$XDG_CONFIG_HOME/git/config" # git config file
ln -sfv "$git_dir/gitignore" "$XDG_CONFIG_HOME/git/ignore" # global ignore file

# setup gpg key
mkdir -pm 0700 "$GNUPGHOME" # create gpg home directory
echo "pinentry-program /opt/homebrew/bin/pinentry-mac" >> \
     "$GNUPGHOME/gpg-agent.conf"
echo "Passphrase: ${bold}AC#s!7cdSXXP6?hM${clear}"

# import personal key pair
gpg --import "$git_dir/public.key" >/dev/null
gpg --import "$git_dir/private.key" >/dev/null
# import RIT key pair
gpg --import "$git_dir/rit-public.key" >/dev/null
gpg --import "$git_dir/rit-private.key" >/dev/null

# fix owner trust level
gpg --import-ownertrust "$git_dir/gpg-ownertrust" >/dev/null
