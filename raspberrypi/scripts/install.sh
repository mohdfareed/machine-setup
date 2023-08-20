#!/usr/bin/env sh
# Install the required packages for the Raspberry Pi

# update packages
sudo apt update

# machine packages
echo "Installing machine packages..."
sudo apt install -y zsh zsh-syntax-highlighting zsh-autosuggestions git exa bat
sudo apt install -y tmux neovim ripgrep fd-find python3-venv npm
sudo apt upgrade -y

# snap store packages
echo "Installing snap store packages..."
sudo apt install -y snapd
sudo snap install core
sudo snap install btop
sudo snap install nvim --classic
sudo snap install go --classic
sudo snap refresh

# go packages
go install github.com/jesseduffield/lazygit@latest

# clean packages
echo "Cleaning packages..."
sudo apt autoremove -y
