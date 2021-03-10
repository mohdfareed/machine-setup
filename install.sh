#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
gbold='\033[1;32m'

# remove last login time prompt
touch $HOME/.hushlogin

# update submodules
git -C $HOME/.dotfiles submodule update --init

# install homebrew and its forumlae and casks
source $HOME/.dotfiles/scripts/homebrew.sh
source $HOME/.dotfiles/scripts/homebrew_formulae.sh
source $HOME/.dotfiles/scripts/homebrew_casks.sh
# install App Store applications
source $HOME/.dotfiles/scripts/appstore.sh

# create symlinks and resource new zsh profile
source $HOME/.dotfiles/scripts/symlink.sh

# install ruby and its gems
source $HOME/.dotfiles/scripts/ruby.sh

# add custom terminal profile. It has to be set as default manually
echo "\n${bold}Adding new terminal profile...${clear}"
open $HOME/.dotfiles/other/Personal.terminal

echo "\n${gbold}Installation complete!${clear}"
