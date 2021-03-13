#!/usr/bin/env zsh

clear='\033[0m'
bold='\033[1m'
rbold='\033[1;31m'

tput clear
echo "${bold}Installing latest LTS Node version...${clear}"

nvm install --lts
