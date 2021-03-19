#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
gbold='\033[1;32m'

DEVELOPER="$HOME/Developer"
DOTFILES="$DEVELOPER/dotfiles"
notebook="/Users/mohdfareed/Library/Mobile\ Documents/com\~apple\~CloudDocs/\
Notebook"
scripts="$DOTFILES/scripts"
username="mohdfareed" # github username
pat='3b82f82e9087eb0db848fada1b1f239ee43a46db' # github personal access token

echo "${bold}Setting up device...${clear}"
# create Developer folder
mkdir -p $HOME/Developer
# remove last login time prompt
touch $HOME/.hushlogin
# add notebook symlink
if [[ -d $notebook ]]; then ln -siv $notebook $HOME; fi

echo
echo "Cloning dotfiles repo..."

# clone repo and its submodules
git clone https://$username:$pat@github.com/mohdfareed/dotfiles.git $DOTFILES
git -C $DOTFILES submodule update --init

# setup homebrew
source $scripts/homebrew.sh
# setup zsh
source $scripts/zsh.sh
# setup git
source $scripts/git.sh
# setup terminal
source $scripts/terminal_setup.sh

# check if brew is installed
which brew > /dev/null
if [[ $? = 0 ]] ; then
    # install brew's forumlae and casks
    source $scripts/homebrew_formulae.sh
    source $scripts/homebrew_casks.sh
    # install App Store applications
    source $scripts/appstore.sh
    # setup ruby and its gems
    source $scripts/ruby.sh
    # setup nvm
    source $scripts/nvm.sh
fi

echo -e "\a"
echo "${gbold}Installation complete!${clear}"
