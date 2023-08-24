#!/usr/bin/env bash
# Install the required packages for the Raspberry Pi

# update packages
sudo apt update
sudo apt upgrade -y

# shell packages
sudo apt install -y zsh zsh-syntax-highlighting zsh-autosuggestions
sudo apt install -y git exa bat tmux python3-venv code

# vim
sudo apt install -y neovim ripgrep fd-find npm

# snap store
sudo apt install -y snapd
sudo snap install core
sudo snap refresh

# snap packages
sudo snap install docker
sudo snap install nvim --classic
sudo snap install go --classic
sudo snap install btop

# go packages
go install github.com/jesseduffield/lazygit@latest

# clean packages
echo "Cleaning packages..."
sudo apt autoremove -y
