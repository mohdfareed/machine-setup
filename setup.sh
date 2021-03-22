#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
gbold='\033[1;32m'

DEV="$HOME/Developer"
DOTFILES="$DEV/dotfiles"

scripts="$DOTFILES/scripts"
username="mohdfareed" # github username
pat='3b82f82e9087eb0db848fada1b1f239ee43a46db' # github personal access token

echo
echo "Cloning dotfiles repo..."
# clone repo and its submodules
git clone https://$username:$pat@github.com/mohdfareed/dotfiles.git $DOTFILES
git -C $DOTFILES submodule update --init

tput clear
echo "${bold}Setting up device...${clear}"

# setup homebrew and install its formulae and casks
source $scripts/homebrew.sh
# install App Store applications
source $scripts/appstore.sh

# setup zsh
source $scripts/zsh.sh
# setup terminal
source $scripts/terminal_setup.sh
# setup git
source $scripts/git.sh

echo -e "\a"
echo "Would you like to setup ${gbold}python${clear}? [Y|n]"
read answer

case $answer in
    [Nn]* ) ;;
    * ) source $scripts/python.sh;;
esac

echo -e "\a"
echo "Would you like to setup ${gbold}rbenv${clear}? [Y|n]"
read answer

case $answer in
    [Nn]* ) ;;
    * ) source $scripts/rbenv.sh;;
esac

echo -e "\a"
echo "Would you like to setup ${gbold}nvm${clear}? [Y|n]"
read answer

case $answer in
    [Nn]* ) ;;
    * ) source $scripts/nvm.sh;;
esac

echo -e "\a"
echo "Restart Terminal app for the changes to take effect."
echo "${gbold}Installation complete!${clear}"
