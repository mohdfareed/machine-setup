#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
gbold='\033[1;32m'

# remove last login time prompt
touch $HOME/.hushlogin

# create config hidden folder
mkdir -p $HOME/.config

# update submodules
git -C $HOME/.dotfiles submodule update --init

# installing oh-my-zsh
source $HOME/.dotfiles/scripts/on_my_zsh.sh

# create symlinks and resource new zsh profile
source $HOME/.dotfiles/scripts/symlink.sh

# install homebrew and its forumlae and casks
source $HOME/.dotfiles/scripts/homebrew.sh
source $HOME/.dotfiles/scripts/homebrew_formulae.sh
source $HOME/.dotfiles/scripts/homebrew_casks.sh
# install App Store applications
source $HOME/.dotfiles/scripts/appstore.sh

# install ruby and its gems
source $HOME/.dotfiles/scripts/ruby.sh

# setup terminal
source $HOME/.dotfiles/scripts/terminal_setup.sh

echo -e "\a"
echo "${gbold}Installation complete!${clear}"
