#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
gbold='\033[1;32m'

dotfiles="$DEVELOPER/dotfiles"
scripts="$dotfiles/scripts"
username="mohdfareed" # github username
pat='3b82f82e9087eb0db848fada1b1f239ee43a46db' # github personal access token


# create Developer folder
mkdir -p $HOME/Developer
# remove last login time prompt
touch $HOME/.hushlogin
# add notebook symlink
ln -siv /Users/mohdfareed/Library/Mobile\ Documents/com\~apple\~CloudDocs/\
Notebook $HOME

# clone repo and its submodules
git clone https://$username:$pat@github.com/mohdfareed/dotfiles.gi $dotfiles
git -C $dotfiles submodule update --init

# setup zsh
source $scripts/zsh.sh

# setup homebrew and its forumlae and casks
source $scripts/homebrew.sh
source $scripts/homebrew_formulae.sh
source $scripts/homebrew_casks.sh
# install App Store applications
source $scripts/appstore.sh

# setup ruby and its gems
source $scripts/ruby.sh

# setup git
source $scripts/git.sh

# setup terminal
source $scripts/terminal_setup.sh

echo -e "\a"
echo "${gbold}Installation complete!${clear}"
