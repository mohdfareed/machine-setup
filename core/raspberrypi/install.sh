# Install the required packages for the Raspberry Pi

# machine packages
echo "Installing machine packages..."
sudo apt update
sudo apt install -y git zsh zsh-syntax-highlighting zsh-autosuggestions
sudo apt install -y bat exa micro code snapd
sudo apt full-upgrade -y

# snap store packages
echo "Installing snap store packages..."
sudo snap install core
sudo snap install docker
sudo snap install btop
sudo snap refresh

# pure prompt
echo "Installing pure prompt..."
mkdir -p $HOME/.zsh
rm -rf $HOME/.zsh/pure
git clone https://github.com/sindresorhus/pure.git $HOME/.zsh/pure

# oh-my-zsh
echo "Installing oh-my-zsh..."
sh -c "$(curl -fsSL https://git.io/JvzfK)" "" --unattended

# tailscale, if not installed
if ! command -v tailscale &> /dev/null; then
    echo "Installing tailscale..."
    curl -fsSL https://tailscale.com/install.sh | sh
fi

# clean packages
echo "Cleaning packages..."
sudo apt autoremove -y
