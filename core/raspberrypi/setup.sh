# Set up a Raspberry Pi with the required packages and configuration

. $HOME/machine/scripts/install.sh # install packages
sudo chsh -s $(which zsh)          # set zsh as the default shell
touch "$HOME/.hushlogin"           # remove login message

# symlink config files
echo "Configuring machine..."
sudo mkdir -p $HOME/.config/micro
sudo ln -sf $HOME/machine/micro_settings.json $HOME/.config/micro/settings.json
sudo ln -sf $HOME/machine/zshrc               $HOME/.zshrc

# load system services
echo "Loading system services..."
for service in ~/machine/*.service; do
    sudo ln -sf $service /etc/systemd/system/$(basename $service)
    sudo systemctl daemon-reload
    sudo systemctl enable $(basename $service)
    sudo systemctl start $(basename $service)
    echo "Loaded $service"
done

# setup docker
echo "Loading Docker..."
sudo snap enable docker
sudo addgroup --system docker && sudo adduser $USER docker
echo "Loading containers..."
cd $HOME/machine && docker compose up -d

# setup zsh and tailscale
echo "Setting up Tailscale..."
sudo tailscale up --accept-dns=false # login to tailscale

# reboot
echo "Done! Rebooting..."
# sudo reboot
