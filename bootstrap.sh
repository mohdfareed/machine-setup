#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

mkdir -p "$HOME/Developer"
DOTFILES="$HOME/Developer/dotfiles"

username="mohdfareed"                          # github username
pat="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" # github personal access token

tput clear
echo "Cloning dotfiles repo..."

# clone repo and its submodules
git clone https://$username:$pat@github.com/mohdfareed/dotfiles.git "$DOTFILES"
git -C "$DOTFILES" submodule update --init --recursive

cd "$DOTFILES"
source "macos/homebrew.sh" # setup homebrew
source "zsh/zsh.sh"        # setup zsh
source "git/git.sh"        # setup git
source "asdf/asdf.sh"      # setup asdf
source "macos/appstore.sh" # install apps from appstore
source "macos/macos.sh"    # setup macos preferences

echo -e "\a"
echo "Restart for some of the changes to take effect."
echo "${bold}Setup complete!${clear}"
