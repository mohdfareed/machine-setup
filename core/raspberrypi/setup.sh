# REQUIREMENTS: $MACHINE is set to the path of the config files to symlink

# remove login message
touch "$HOME/.hushlogin"

# install packages
. $MACHINE/install.sh

# symlink config files
ln -sf $MACHINE/micro_settings.json $HOME/.config/micro/settings.json
ln -sf $MACHINE/zshrc               $HOME/.zshrc

# set zsh as the default shell
sudo chsh -s $(which zsh)
