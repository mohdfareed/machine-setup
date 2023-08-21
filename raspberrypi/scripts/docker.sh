#!/usr/bin/env bash
# Install docker and run containers

echo "Installing Docker..."
sudo snap install docker
sudo snap refresh docker
sudo snap enable docker
sudo addgroup --system docker && sudo adduser $USER docker
echo "Run 'compose-machine up -d' to load containers after reboot"
