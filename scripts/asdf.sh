#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
source $DOTFILES/dots/zshenv

# link asdfrc
mkdir -p $(dirname $ASDF_CONFIG_FILE)
ln -siv "$DOTFILES/dots/asdfrc" "$ASDF_CONFIG_FILE"

# python setup
# ============

tput clear
echo "${bold}Setting up python...${clear}"
# link pythonrc
mkdir -p $(dirname $PYTHONSTARTUP)
ln -siv "$DOTFILES/dots/pythonrc" "$PYTHONSTARTUP"
# installed latest python version and set it as default
asdf plugins add python
asdf install python latest > /dev/null
asdf global python latest

# ruby setup
# ==========

echo
echo "${bold}Setting up ruby...${clear}"
gem install solargraph # code completion, documentation, and static analysis
gem install ruby-debug-ide # an interface which glues ruby-debug to IDEs
gem install debase -v '>= 0.2.5.beta' # implementation of standard Ruby debugger
# installed latest ruby version and set it as default
asdf plugin add ruby
asdf install ruby latest > /dev/null
asdf global ruby latest

# node setup
# ==========

echo
echo "${bold}Setting up nvm...${clear}"
# create needed directories
mkdir -p $(dirname $NPM_CONFIG_USERCONFIG)
mkdir -p $(dirname $NODE_REPL_HISTORY)
mkdir -p $NPM_CONFIG_CACHE
# installed latest node version and set it as default
asdf plugin add nodejs
asdf install nodejs latest > /dev/null
asdf global nodejs latest

# sqlite setup
# ============

echo
echo "${bold}Setting up sqlite...${clear}"
mkdir -p $(dirname $SQLITE_HISTORY) # create history directory
# installed latest sqlite version and set it as default
asdf plugin add sqlite
asdf install sqlite latest > /dev/null
asdf global sqlite latest

# postgresql setup
# ============

echo
echo "${bold}Setting up postgresql...${clear}"
# create needed directories
mkdir $(dirname $PSQLRC)
mkdir $(dirname $PSQL_HISTORY)
#  compile with openssl libraries
POSTGRES_EXTRA_CONFIGURE_OPTIONS="--with-uuid=e2fs --with-openssl \
--with-libraries=/usr/local/lib:$(brew --prefix openssl)/lib \
--with-includes=/usr/local/include:$(brew --prefix openssl)/include"
# installed latest postgresql version and set it as default
asdf plugins add postgres
asdf install postgres latest > /dev/null
asdf global postgres latest

asdf reshim
