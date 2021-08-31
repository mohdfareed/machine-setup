#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'

tput clear
echo "${bold}Setting up ruby...${clear}"

# installed latest ruby version and set it as default
asdf plugin add ruby
asdf install ruby latest > /dev/null
asdf global ruby latest

# install gems

gem install bundler # manages an app's dependencies through its entire life
gem install pry     # runtime developer console and IRB alternative
gem install byebug  # ruby debugger

gem install solargraph     # code completion, documentation, and static analysis
gem install ruby-debug-ide # an interface which glues ruby-debug to IDEs
gem install debase -v '>= 0.2.5.beta' # implementation of standard Ruby debugger

asdf reshim
