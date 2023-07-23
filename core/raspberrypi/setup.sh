# remove login message
touch "$HOME/.hushlogin"
# install packages
. ~/machine/install.sh

# symlink config files
ln -sf ~/machine/zshrc               $HOME/.zshrc
ln -sf ~/machine/micro_settings.json $HOME/.config/micro/settings.json
ln -sf ~/machine/file_share.conf     /etc/samba/smb.conf

# load services
for service in ~/machine/*.service; do
    sudo ln -sf $service /etc/systemd/system/$(basename $service)
    sudo systemctl daemon-reload
    sudo systemctl enable $(basename $service)
done

# set zsh as the default shell
sudo chsh -s $(which zsh)
