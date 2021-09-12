#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up python...${clear}"

python_dir=$(dirname $0)
source $(dirname $python_dir)/zsh/zshenv

# symlink python startup file
mkdir -p $(dirname $PYTHONSTARTUP)
ln -siv "$python_dir/pythonrc" "$PYTHONSTARTUP"

# installed latest python version and set it as default
asdf plugin add python
asdf install python latest > /dev/null
asdf global python latest
asdf reshim

# add environment variables
cat env_vars >> $ZDOTDIR/env_vars
echo >> $ZDOTDIR/env_vars
