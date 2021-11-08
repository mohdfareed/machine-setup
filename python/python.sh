#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up python...${clear}"

python_dir=$(dirname "${0:a}")
source "$(dirname "$python_dir")/zsh/zshenv"

# add environment variables
cat "$python_dir/env_vars" >>"$ZDOTDIR/env_vars"
echo >>"$ZDOTDIR/env_vars"
source "$(dirname "$python_dir")/zsh/zshenv"

# symlink python startup file
mkdir -p "$(dirname "$PYTHONSTARTUP")"
ln -sfv "$python_dir/pythonrc" "$PYTHONSTARTUP"

# installed latest python version and set it as default
asdf plugin add python
asdf install python latest >/dev/null
asdf global python latest
asdf reshim
