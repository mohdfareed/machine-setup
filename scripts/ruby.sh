#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'
gbold='\033[1;32m'

tput clear
echo "${bold}Setting up ruby...${clear}"

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

# install ruby and rbenv
brew install ruby
brew install rbenv
brew cleanup

# add gems directory to path
gemdir="$(gem environment gemdir)/"
currdir='/usr/local/lib/ruby/gems/.*/'
sed -i '' "s#$currdir#$gemdir#" "$DOTFILES/dots/zshrc"

echo "${bold}Installing gems...${clear}"

# code completion, documentation, and static analysis
gem install solargraph
# an interface which glues ruby-debug to IDEs
gem install ruby-debug-ide
# fast implementation of the standard Ruby debugger
gem install debase -v '>= 0.2.5.beta'
# CLI gem that beautifies the terminal's ls command, with color and icons
gem install colorls

# link colorls configuration
mkdir -p $XDG_CONFIG_HOME/colorls
ln -siv $DOTFILES/other/dark_colors.yaml \
    $XDG_CONFIG_HOME/colorls/dark_colors.yaml

# get path of file specifying config dir and update it
colorls_path="$(dirname $(gem which colorls))/colorls/yaml.rb"
sed -i '' "s#.config/colorls#$XDG_CONFIG_HOME/colorls#" $colorls_path


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

prompt pry      # runtime developer console and IRB alternative
prompt byebug   # Ruby debugger
prompt rails    # full-stack web framework
prompt colorize # methods to set text color, background color, text effects

gem update
