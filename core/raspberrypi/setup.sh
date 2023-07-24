# remove login message
touch "$HOME/.hushlogin"
# install packages
. $HOME/machine/install.sh

# symlink config files
sudo ln -sf $HOME/machine/zshrc               $HOME/.zshrc
sudo ln -sf $HOME/machine/micro_settings.json $HOME/.config/micro/settings.json
sudo ln -sf $HOME/machine/nginx.config        /etc/nginx/sites-enabled/default

# load services
for service in ~/machine/*.service; do
    sudo ln -sf $service /etc/systemd/system/$(basename $service)
    sudo systemctl daemon-reload
    sudo systemctl enable $(basename $service)
done

# load dashboard
pushd $HOME/machine/dashboard && sudo docker compose up -d && popd
# setup tailscale
sudo tailscale up --accept-dns=false--authkey $TAILSCALE_AUTHKEY
# setup adguard
sudo adguard -s install

# set zsh as the default shell
sudo chsh -s $(which zsh)

# instructions
echo "Done! Please reboot your machine."
echo "Set tailscale global dns to $(tailscale ip -4)"
echo "Setup adguard at http://$(tailscale ip -4):3000"
