#!/usr/bin/env sh
# Install the required packages for the Raspberry Pi

# update packages
sudo apt update

# machine packages
echo "Installing machine packages..."
sudo apt install -y git zsh zsh-syntax-highlighting zsh-autosuggestions
sudo apt install -y exa bat micro neovim snapd
sudo apt upgrade -y

# snap store packages
echo "Installing snap store packages..."
sudo snap install core
sudo snap install btop
sudo snap refresh

# clean packages
echo "Cleaning packages..."
sudo apt autoremove -y
