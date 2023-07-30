# Set up a Raspberry Pi with the required packages and configuration

# remove login message
touch "$HOME/.hushlogin"

# symlink config files
echo "Symlinking config files..."
sudo ln -sf $HOME/machine/zshrc               $HOME/.zshrc
sudo ln -sf $HOME/machine/micro_settings.json $HOME/.config/micro/settings.json

# install packages
echo "Installing packages..."
. $HOME/machine/scripts/install.sh

# load docker containers
echo "Loading docker containers..."
sudo usermod -aG docker $USER
cd $HOME/machine && sudo docker compose up -d

# load system services
echo "Loading system services..."
for service in ~/machine/*.service; do
    sudo ln -sf $service /etc/systemd/system/$(basename $service)
    sudo systemctl daemon-reload
    sudo systemctl enable $(basename $service)
    sudo systemctl start $(basename $service)
    echo "Loaded $service"
done

# setup zsh and tailscale then reboot
sudo chsh -s $(which zsh)            # set zsh as the default shell
sudo tailscale up --accept-dns=false # login to tailscale
echo "Done! Rebooting..."
sudo reboot
