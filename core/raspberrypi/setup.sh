# remove login message
touch "$HOME/.hushlogin"

# symlink config files
sudo ln -sf $HOME/machine/zshrc               $HOME/.zshrc
sudo ln -sf $HOME/machine/micro_settings.json $HOME/.config/micro/settings.json
# install packages
. $HOME/machine/scripts/install.sh

# load docker containers and services
sudo usermod -aG docker $USER
pushd $HOME/machine && sudo docker compose up -d && popd
for service in ~/machine/*.service; do
    sudo ln -sf $service /etc/systemd/system/$(basename $service)
    sudo systemctl daemon-reload
    sudo systemctl enable $(basename $service)
done


sudo tailscale up --accept-dns=false # setup tailscale
sudo chsh -s $(which zsh)            # set zsh as the default shell
echo "Done! Please reboot your machine."
