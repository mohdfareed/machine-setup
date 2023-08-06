#!/usr/bin/env sh
# Configure the shell for the Raspberry Pi

# symlink config files
echo "Configuring machine..."
sudo mkdir -p $HOME/.config/micro
sudo ln -sf $MACHINE/micro_settings.json $HOME/.config/micro/settings.json
sudo ln -sf $MACHINE/zshrc               $HOME/.zshrc
sudo ln -sf $MACHINE/zshenv              $HOME/.zshenv
sudo ln -sf $MACHINE/zprofile            $HOME/.zprofile

# change default shell to zsh
sudo chsh -s $(which zsh)
# remove login message
touch "$HOME/.hushlogin"

# oh-my-zsh
echo "Installing oh-my-zsh..."
mkdir -p $HOME/.zsh
sh -c "$(curl -fsSL https://git.io/JvzfK)"

# auto completion
echo "Installing zsh-completions prompt..."
completions=$HOME/.zsh/zsh-completions; rm -rf $completions
git clone https://github.com/zsh-users/zsh-completions $completions

# pure prompt
echo "Installing pure prompt..."
pure=$HOME/.zsh/pure; rm -rf $pure
git clone https://github.com/sindresorhus/pure.git $pure
