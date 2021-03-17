#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
gbold='\033[1;32m'

echo "${bold}Updating...${clear}"

# update submodules
git -C $DOTFILES submodule update --init

# update brew and its forumlae and casks
which brew > /dev/null
if [[ $? = 0 ]] ; then
    brew update
    brew upgrade
    brew cleanup
fi
# update App Store applications
which mas > /dev/null
if [[ $? = 0 ]] ; then
    mas upgrade
fi

# update oh-my-zsh
which omz > /dev/null
if [[ $? = 0 ]] ; then
    omz update
fi

# install latest ruby version
which rbenv > /dev/null
if [[ $? = 0 ]] ; then
    source $DOTFILES/scripts/ruby.sh
fi

# install latest Node version
which nvm > /dev/null
if [[ $? = 0 ]] ; then
    source $DOTFILES/scripts/nvm.sh
fi

echo "${gbold}Updating complete!${clear}"
