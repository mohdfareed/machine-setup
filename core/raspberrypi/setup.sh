# REQUIREMENTS: $MACHINE set to the path of the machine resource directory

# remove login message
touch "$HOME/.hushlogin"
# install packages
. $MACHINE/install.sh

# symlink config files
ln -sf $MACHINE/micro_settings.json $HOME/.config/micro/settings.json
ln -sf $MACHINE/zshrc               $HOME/.zshrc
# load services
for service in $MACHINE/*.service; do
    sudo ln -sf $service /etc/systemd/system/$(basename $service)
done

# set zsh as the default shell
sudo chsh -s $(which zsh)
