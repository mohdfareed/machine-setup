# Install the required packages for the Raspberry Pi

# machine packages
sudo apt update && sudo apt full-upgrade -y
echo "Installing machine packages..."
sudo apt install git zsh zsh-syntax-highlighting zsh-autosuggestions -y
sudo apt install bat exa micro code snapd -y

# snap store packages
sudo snap install core
sudo snap install docker
sudo snap install btop

# pure prompt
echo "Installing pure prompt..."
mkdir -p $HOME/.zsh
rm -rf $HOME/.zsh/pure
git clone https://github.com/sindresorhus/pure.git $HOME/.zsh/pure

# oh-my-zsh
echo "Installing oh-my-zsh..."
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
      "" --unattended

# tailscale
echo "Installing tailscale..."
curl -fsSL https://tailscale.com/install.sh | sh

# clean packages
echo "Cleaning packages..."
sudo apt autoremove -y
