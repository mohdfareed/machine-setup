#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up ruby...${clear}"

ruby_dir=$(dirname "${0:a}")
source "$(dirname "$ruby_dir")/zsh/zshenv"

# add environment variables
cat "$ruby_dir/env_vars" >>"$ZDOTDIR/env_vars"
echo >>"$ZDOTDIR/env_vars"
source "$(dirname "$ruby_dir")/zsh/zshenv"

# set default gems
ln -sfv "$ruby_dir/default-gems" "$ASDF_GEM_DEFAULT_PACKAGES_FILE"

# installed latest ruby version and set it as default
asdf plugin add ruby
asdf install ruby latest >/dev/null
asdf global ruby latest
asdf reshim
