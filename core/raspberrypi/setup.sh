# Set up a Raspberry Pi with the required packages and configuration

# install packages
. $HOME/machine/scripts/install.sh

# symlink config files
echo "\nConfiguring machine..."
sudo mkdir -p $HOME/.config/micro
sudo ln -sf $HOME/machine/micro_settings.json $HOME/.config/micro/settings.json
sudo ln -sf $HOME/machine/zshrc               $HOME/.zshrc
touch "$HOME/.hushlogin" # remove login message

# load system services
echo "\nLoading system services..."
for service in ~/machine/*.service; do
    sudo ln -sf $service /etc/systemd/system/$(basename $service)
    sudo systemctl daemon-reload
    sudo systemctl enable $(basename $service)
    sudo systemctl start $(basename $service)
    echo "Loaded $service"
done

# setup docker
sudo snap disable docker &&  snap enable docker
sudo addgroup --system docker &&  adduser $USER docker
# load containers
newgrp docker
echo "\nLoading containers..."
cd $HOME/machine && sudo docker compose up -d

# setup zsh and tailscale
echo "Setting up tailscale..."
sudo tailscale up --accept-dns=false # login to tailscale
sudo chsh -s $(which zsh)            # set zsh as the default shell
# reboot
echo "Done! Rebooting..."
sudo reboot
