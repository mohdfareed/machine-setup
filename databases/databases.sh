#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

# sqlite setup
# ============

tput clear
echo "${bold}Setting up sqlite...${clear}"

db_dir=$(dirname "$0")
source "$(dirname "$db_dir")/zsh/zshenv"
mkdir -p "$(dirname "$SQLITE_HISTORY")" # create history directory

# installed latest sqlite version and set it as default
asdf plugin add sqlite
asdf install sqlite latest > /dev/null
asdf global sqlite latest
asdf reshim

# add environment variables
cat "$db_dir/sqlite_env_vars" >> "$ZDOTDIR/env_vars"
echo >> "$ZDOTDIR/env_vars"

# postgresql setup
# ============

echo
echo "${bold}Setting up postgresql...${clear}"

# create needed directories
mkdir "$(dirname "$PSQLRC")"
mkdir "$(dirname "$PSQL_HISTORY")"

#  compile with openssl libraries
POSTGRES_EXTRA_CONFIGURE_OPTIONS="--with-uuid=e2fs --with-openssl \
--with-libraries=/usr/local/lib:$(brew --prefix openssl)/lib \
--with-includes=/usr/local/include:$(brew --prefix openssl)/include"

# installed latest postgresql version and set it as default
asdf plugin add postgres
asdf install postgres latest > /dev/null
asdf global postgres latest
asdf reshim

# add environment variables
cat "$db_dir/psql_env_vars" >> "$ZDOTDIR/env_vars"
echo >> "$ZDOTDIR/env_vars"
