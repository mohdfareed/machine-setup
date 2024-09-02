# update packages
sudo apt update
sudo apt upgrade -y

# snap store
sudo apt install -y snapd
sudo snap install core
sudo snap refresh

# docker
sudo snap install docker

# npm
sudo apt install -y npm

# vscode
sudo apt install -y code

# clean packages
sudo apt autoremove -y
