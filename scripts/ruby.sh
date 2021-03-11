#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

# prompt the user for confirmation, skip installation if needed
prompt() {
    echo "\nWould you like to install ${rbold}$1${clear}? [Y|n]"
    read answer

    case $answer in
        [Nn]* )
            ;;
        * )
            gem install $1;;
    esac
}


tput clear
echo "${bold}Installing latest version of Ruby...${clear}"

# get the latest version number of Ruby
version=$(rbenv install -l 2> /dev/null | grep -v '-' | tail -1)

# prompt the user for confirmation to install latest ruby version

echo "\nRuby version ${rbold}$version${clear} will be installed."
echo
read -sk "?Press RETURN to continue or any other key to abort" answer

if [[ $answer = $'\n' ]] ; then
    # installed latest Ruby version and set it as default
    rbenv install $version
    rbenv global $version
    rbenv rehash

    echo "${bold}Installing gems...${clear}"

    # prompt the user to choose the gems to install
    prompt bundler  # applications' dependencies manager
    prompt pry      # runtime developer console and IRB alternative
    prompt byebug   # Ruby debugger
    prompt rails    # full-stack web framework
    prompt colorize # methods to set text color, background color, text effects
    prompt colorls  # CLI gem that beautifies the terminal's ls command
fi
