#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
gbold='\033[1;32m'

DEV="$HOME/Developer"
DOTFILES="$DEV/dotfiles"

scripts="$DOTFILES/scripts"
username="mohdfareed" # github username
pat='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' # github personal access token

tput clear
echo "${bold}Setting up device...${clear}"

echo
echo "Cloning dotfiles repo..."
# clone repo and its submodules
git clone https://$username:$pat@github.com/mohdfareed/dotfiles.git $DOTFILES
git -C $DOTFILES submodule update --init

# setup homebrew and install its formulae and casks
source $scripts/homebrew.sh
# install App Store applications
source $scripts/appstore.sh
# setup zsh
source $scripts/zsh.sh
# setup git
source $scripts/git.sh

echo -e "\a"
echo "Would you like to setup ${gbold}Python${clear}? [Y|n]"
read answer

case $answer in
    [Nn]* ) ;;
    * ) source $scripts/python.sh;;
esac

echo -e "\a"
echo "Would you like to setup ${gbold}Ruby${clear}? [Y|n]"
read answer

case $answer in
    [Nn]* ) ;;
    * ) source $scripts/ruby.sh;;
esac

echo -e "\a"
echo "Would you like to setup ${gbold}nvm${clear}? [Y|n]"
read answer

case $answer in
    [Nn]* ) ;;
    * ) source $scripts/nvm.sh;;
esac

# setup macOS preferences
source $scripts/macos.sh

echo -e "\a"
echo "Restart for some of the changes to take effect."
echo "${gbold}Setup complete!${clear}"
