#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
gbold='\033[1;32m'

echo "${bold}Updating...${clear}"

# update submodules
git -C $DEVELOPER/dotfiles submodule update --init

# update brew and its forumlae and casks
which -s brew
if [[ $? = 0 ]] ; then
    brew update
    brew upgrade
    brew cleanup
fi

which -s mas
if [[ $? = 0 ]] ; then
    mas upgrade
fi

# install latest ruby version
which -s rbenv
if [[ $? = 0 ]] ; then
    source $DEVELOPER/dotfiles/scripts/ruby.sh
    gem update
fi

# update oh-my-zsh
which -s omz
if [[ $? = 0 ]] ; then
    omz update
fi

echo "${gbold}Updating complete!${clear}"
