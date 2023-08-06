#!/usr/bin/env sh
# Install docker and run containers

echo "Installing Docker..."
sudo snap install docker
sudo snap refresh docker
sudo snap enable docker

echo "Loading containers..."
sudo addgroup --system docker && sudo adduser $USER docker
cd $HOME/machine && docker compose up -d
