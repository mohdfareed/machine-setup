#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'
gbold='\033[1;32m'

tput clear
echo "${bold}Setting up python...${clear}"

# check if brew is installed
which brew > /dev/null
if [[ $? != 0 ]] ; then
    echo "${rbold}Error:${clear} Homebrew is not installed..."
    return 1
fi
# check if DOTFILES directory exists
if [[ ! -d $DOTFILES ]] ; then
    echo "${rbold}Error:${clear} DOTFILES directory does not exist..."
    return 1
fi

# source zshenv and zshrc
source $DOTFILES/dots/zshenv
source $DOTFILES/dots/zshrc > /dev/null

# install python and pyenv
brew install python
brew cleanup

# link pythonrc
mkdir -p $XDG_CONFIG_HOME/python
ln -siv "$DOTFILES/dots/pythonrc" "$PYTHONSTARTUP"

# prompt the user for confirmation to install pyenv
echo -e "\a"
echo "Would you like to install ${gbold}pyenv${clear}? [Y|n]"
read answer

case $answer in
        [Nn]* )
            return 1
            ;;
        * )
            ;;
esac

brew install pyenv
brew cleanup
