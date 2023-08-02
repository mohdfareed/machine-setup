# Set up a Raspberry Pi with the required packages and configuration

touch "$HOME/.hushlogin"           # remove login message
. $HOME/machine/scripts/install.sh # install packages

# symlink config files
echo "Configuring machine..."
sudo mkdir -p $HOME/.config/micro
sudo ln -sf $HOME/machine/micro_settings.json $HOME/.config/micro/settings.json
sudo ln -sf $HOME/machine/zshrc               $HOME/.zshrc
sudo ln -sf $HOME/machine/zshenv              $HOME/.zshenv
# change default shell to zsh
sudo chsh -s $(which zsh)
sudo exec zsh

# load system services
echo "Loading system services..."
for service in ~/machine/*.service; do
    sudo ln -sf $service /etc/systemd/system/$(basename $service)
    sudo systemctl daemon-reload
    sudo systemctl enable $(basename $service)
    sudo systemctl start $(basename $service)
    echo "Loaded $service"
done

# setup tailscale
. $HOME/machine/scripts/tailscale.sh
# setup docker
. $HOME/machine/scripts/docker.sh

# reboot
echo "Add the following DNS nameserver to Tailscale DNS settings:"
echo "    Nameserver: $(tailscale ip -1)"
echo "    Restrict to Domain: pi"
echo "Done! Rebooting..."
# sudo reboot
