#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

DOTFILES="$HOME/Developer/dotfiles"

username="mohdfareed"                          # github username
pat="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" # github personal access token

tput clear
echo "Cloning dotfiles repo..."
# clone repo and its submodules
git clone https://$username:$pat@github.com/mohdfareed/dotfiles.git $DOTFILES
git -C $DOTFILES submodule update --init

cd "$DOTFILES"
cd - > /dev/null

echo -e "\a"
echo "Restart for some of the changes to take effect."
echo "${bold}Setup complete!${clear}"
