#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'
gbold='\033[1;32m'

# prompt the user for confirmation, skip installation if needed
prompt() {
    echo -e "\a"
    echo "Would you like to install ${gbold}$1${clear}? [Y|n]"
    read answer

    case $answer in
        [Nn]* )
            ;;
        * )
            gem install $1
            ;;
    esac
}


tput clear
echo "${bold}Setting up rbenv...${clear}"

# check if brew is installed
which brew > /dev/null
if [[ $? != 0 ]] ; then
    echo "${rbold}Error:${clear} Homebrew is not installed..."
    return 1
fi

brew install ruby
brew install rbenv
brew cleanup

if [[ ! -d $DOTFILES ]] ; then
    echo "${rbold}Error:${clear} DOTFILES directory does not exist..."
    return 1
fi

source $DOTFILES/dots/zshenv
source $DOTFILES/dots/zshrc > /dev/null

# prompt the user to selected ruby version to install
echo -e "\a"
echo "Which ruby version would you like to install?"
echo
echo "${bold}Installed versions:${clear}"
rbenv versions
echo "${bold}Available versions:${clear}"
rbenv install -l 2> /dev/null
read version

# install selected Ruby version and set it as default
rbenv install $version
if [[ $? != 0 ]] ; then
    return 1
fi
rbenv global $version
rbenv rehash
eval "$(rbenv init -)" # update the current session's ruby

echo "${bold}Installing gems...${clear}"

prompt pry      # runtime developer console and IRB alternative
prompt byebug   # Ruby debugger
prompt rails    # full-stack web framework
prompt colorize # methods to set text color, background color, text effects

# vscode functionality
gem install solargraph # code completion, documentation, and static analysis
gem install ruby-debug-ide # an interface which glues ruby-debug to IDEs
gem install debase -v 0.2.5.beta2 # fast implementation of the standard Ruby debugger

gem update
