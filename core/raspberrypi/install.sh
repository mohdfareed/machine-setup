# Install the required packages for the Raspberry Pi

# machine packages
echo "Installing machine packages..."
sudo apt update
sudo apt install git zsh zsh-syntax-highlighting zsh-autosuggestions -y
sudo apt install bat exa micro code snapd -y
sudo apt full-upgrade -y

# snap store packages
echo "Installing snap store packages..."
sudo snap install core
sudo snap install docker
sudo snap install btop
sudo snap refresh

# pure prompt
echo "\nInstalling pure prompt..."
mkdir -p $HOME/.zsh
rm -rf $HOME/.zsh/pure
git clone https://github.com/sindresorhus/pure.git $HOME/.zsh/pure

# oh-my-zsh
echo "\nInstalling oh-my-zsh..."
sh -c "$(curl -fsSL https://git.io/JvzfK)" "" --unattended

# tailscale
echo "\nInstalling tailscale..."
curl -fsSL https://tailscale.com/install.sh | sh

# clean packages
echo "\nCleaning packages..."
sudo apt autoremove -y
