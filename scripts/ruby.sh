#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

# prompt the user for confirmation, skip installation if needed
prompt() {
    echo -e "\a"
    echo "Would you like to install ${rbold}$1${clear}? [Y|n]"
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
echo "${bold}Installing rbenv and latest version of Ruby...${clear}"

# check if brew is installed before installing rbenv
which brew > /dev/null
if [[ $? != 0 ]] ; then
    echo "${bold}Homebrew is not installed...${clear}"
    return 1
fi

brew install rbenv

# get the latest version number of Ruby
version=$(rbenv install -l 2> /dev/null | grep -v '-' | tail -1)

# prompt the user for confirmation to install latest ruby version
echo -e "\a"
echo "Would you like to install Ruby version ${rbold}$version${clear}? [Y|n]"
read answer

case $answer in
        [Yy]* )
            ;;
        * )
            # installed latest Ruby version and set it as default
            rbenv install $version
            rbenv global $version
            rbenv rehash
            eval "$(rbenv init -)" # update the current session's ruby
            ;;
esac

echo "${bold}Installing gems...${clear}"

prompt bundler  # applications' dependencies manager
prompt pry      # runtime developer console and IRB alternative
prompt byebug   # Ruby debugger
prompt rails    # full-stack web framework
prompt colorize # methods to set text color, background color, text effects

# vscode functionality
prompt solargraph # code completion, documentation, and static analysis
prompt ruby-debug-ide # an interface which glues ruby-debug to IDEs
prompt debase -v 0.2.5.beta2 # fast implementation of the standard Ruby debugger

gem update
