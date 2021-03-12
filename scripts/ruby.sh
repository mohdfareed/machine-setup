#!/usr/bin/env zsh

## REQUIREMENTS:
# brew
# rbenv

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
            gem install $1;;
    esac
}


tput clear
echo "${bold}Installing latest version of Ruby...${clear}"

# check if rbenv is installed
which -s rbenv
if [[ $? != 0 ]] ; then
    echo "${bold}rbenv is not installed.${clear}"
    echo "${bold}Would you like to install it?${clear}"
    echo -e "\a"
    read -sk "?Press RETURN to continue or any other key to abort" answer

    if [[ $answer != $'\n' ]] ; then
    exit;
    fi

    # check if brew is installed before installing rbenv
    which -s brew
    if [[ $? != 0 ]] ; then
        echo "${bold}Homebrew is not installed.${clear}"
        echo "${bold}Would you like to install it?${clear}"
        echo -e "\a"
        read -sk "?Press RETURN to continue or any other key to abort" answer

        if [[ $answer != $'\n' ]] ; then
        exit;
        fi

        source $dotfiles/scripts/homebrew.sh
    fi

    brew install rbenv
fi

# get the latest version number of Ruby
version=$(rbenv install -l 2> /dev/null | grep -v '-' | tail -1)

# prompt the user for confirmation to install latest ruby version
echo "\nRuby version ${rbold}$version${clear} will be installed."
echo -e "\a"
read -sk "?Press RETURN to continue or any other key to abort" answer

if [[ $answer = $'\n' ]] ; then
    # installed latest Ruby version and set it as default
    rbenv install $version
    rbenv global $version
    rbenv rehash
    eval "$(rbenv init -)" # update the current session's ruby

    echo "${bold}Installing gems...${clear}"

    # prompt the user to choose the gems to install
    prompt bundler  # applications' dependencies manager
    prompt pry      # runtime developer console and IRB alternative
    prompt byebug   # Ruby debugger
    prompt rails    # full-stack web framework
    prompt colorize # methods to set text color, background color, text effects
    prompt colorls  # CLI gem that beautifies the terminal's ls command

    # link colorls config if it is installed
    which -s colorls
    if [[ $? = 0 ]] ; then
        # link colorls configuration
        mkdir -p $HOME/.config/colorls
        ln -siv $HOME/.dotfiles/other/dark_colors.yaml \
        $HOME/.config/colorls/dark_colors.yaml
    fi
fi
