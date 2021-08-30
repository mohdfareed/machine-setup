#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
gbold='\033[1;32m'

DOTFILES="$HOME/Developer/dotfiles"

scripts="$DOTFILES/scripts"
username="mohdfareed" # github username
pat='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' # github personal access token

tput clear
echo "Cloning dotfiles repo..."
# clone repo and its submodules
git clone https://$username:$pat@github.com/mohdfareed/dotfiles.git $DOTFILES
git -C $DOTFILES submodule update --init

source $scripts/homebrew.sh # setup homebrew
source $scripts/zsh.sh      # setup zsh
source $scripts/git.sh      # setup git
source $scripts/asdf.sh     # setup asdf
source $scripts/appstore.sh # install App Store applications
source $scripts/macos.sh    # setup macOS preferences

echo -e "\a"
echo "Restart for some of the changes to take effect."
echo "${gbold}Setup complete!${clear}"
