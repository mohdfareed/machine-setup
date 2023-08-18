#!/usr/bin/env bash
# Configure the shell for the Raspberry Pi

machine=$(dirname "$(realpath $0)")/.. # machine directory
source $machine/zshenv # load environment variables

# oh-my-zsh
echo "Installing oh-my-zsh..."
sh -c "$(curl -fsSL https://git.io/JvzfK)" "" --unattended
sudo rm -f $HOME/.zshrc.pre-oh-my-zsh* &> /dev/null

# auto completion
echo "Installing zsh-completions prompt..." && sudo rm -rf $ZSHCOMP
git clone https://github.com/zsh-users/zsh-completions $ZSHCOMP

# pure prompt
echo "Installing pure prompt..." && sudo rm -rf $PURE
git clone https://github.com/sindresorhus/pure.git $PURE

echo "Configuring machine..."
sudo chsh -s $(which zsh)      # change default shell to zsh
sudo touch "$HOME/.hushlogin"  # remove login message
sudo mkdir -p $HOME/.config    # create config directory

# create symlinks
sudo ln -sf $machine/zprofile  $HOME/.zprofile
sudo ln -sf $machine/zshenv    $HOME/.zshenv
sudo ln -sf $machine/zshrc     $HOME/.zshrc
sudo ln -sf $machine/vim       $HOME/.config/nvim
sudo ln -sf $machine/tmux.conf $HOME/.tmux.conf
