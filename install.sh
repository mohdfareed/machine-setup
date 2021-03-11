#!/usr/bin/env zsh

scripts="$HOME/.dotfiles/scripts"
clear='\033[0m'
bold='\033[1m'
gbold='\033[1;32m'

# remove last login time prompt
touch $HOME/.hushlogin

# create config hidden folder
mkdir -p $HOME/.config

# clone repo
source $scripts/scripts/git.sh

# installing oh-my-zsh
source on_my_zsh.sh

# create symlinks and resource new zsh profile
source $scripts/symlink.sh

# install homebrew and its forumlae and casks
source $scripts/homebrew.sh
source $scripts/homebrew_formulae.sh
source $scripts/homebrew_casks.sh
# install App Store applications
source $scripts/appstore.sh

# install ruby and its gems
source $scripts/ruby.sh

# setup terminal
source $scripts/terminal_setup.sh

echo -e "\a"
echo "${gbold}Installation complete!${clear}"
