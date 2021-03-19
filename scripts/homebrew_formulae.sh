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
        [Nn]* ) ;;
        * ) brew install $1;;
    esac
}


tput clear
echo "${bold}Installing homebrew formulae...${clear}"

# check if brew is installed before installing rbenv
which brew > /dev/null
if [[ $? != 0 ]] ; then
    echo "${bold}Homebrew is not installed.${clear}"
    return 1
fi

# essential formulae

# UNIX shell (command interpreter)
brew install zsh
# Fish shell like syntax highlighting for zsh
brew install zsh-syntax-highlighting
# Distributed revision control system
brew install git
# Interpreted, interactive, object-oriented programming language
prompt python
#Powerful, clean, object-oriented scripting language
prompt ruby

# utilities

# Mac App Store command-line interface
prompt mas
# Play, record, convert, and stream audio and video
prompt ffmpeg # youtube-dl dependency
# Download YouTube videos from the command-line
prompt youtube-dl
# Generic syntax highlighter
prompt pygments

# Markdown Preview Enhanced vscode extension

# Graph visualization software. Used to display graphs in markdown preview
prompt graphviz
# Development kit for the Java programming language
prompt java

brew cleanup

# prompt to install colorls
# CLI gem that beautifies the terminal's ls command
echo -e "\a"
echo "Would you like to install ${rbold}colorls${clear}? [Y|n]"
read answer
case $answer in
    [Nn]* )
        ;;
    * )
        gem install colorls
        ;;
esac

# link colorls config if it is installed and let colorls point to it
which colorls > /dev/null
if [[ $? = 0 ]] ; then
    # link colorls configuration
    mkdir -p $XDG_CONFIG_HOME/colorls
    ln -siv $DOTFILES/other/dark_colors.yaml \
        $XDG_CONFIG_HOME/colorls/dark_colors.yaml

    # get path of file specifying config dir and update it
    colorls_path="$(dirname $(gem which colorls))/colorls/yaml.rb"
    sed -i '' 's#.config/colorls#Developer/colorls#' $colorls_path
fi

# check if java is installed
brew list java > /dev/null
if [[ $? = 0 ]] ; then
    sudo ln -sfn $(brew --prefix)/opt/openjdk/libexec/openjdk.jdk \
        /Library/Java/JavaVirtualMachines/openjdk.jdk
fi
