# Install the required packages for the Raspberry Pi

# machine packages
echo "Installing machine packages..."
sudo apt update
sudo apt install -y git zsh zsh-syntax-highlighting zsh-autosuggestions
sudo apt install -y bat exa micro code snapd
sudo apt upgrade -y

# snap store packages
echo "Installing snap store packages..."
sudo snap install core
sudo snap install btop
sudo snap refresh

# oh-my-zsh
echo "Installing oh-my-zsh..."
sh -c "$(curl -fsSL https://git.io/JvzfK)" "" --unattended

# pure prompt
echo "Installing pure prompt..."
mkdir -p $HOME/.zsh
rm -rf $HOME/.zsh/pure
git clone https://github.com/sindresorhus/pure.git $HOME/.zsh/pure

# clean packages
echo "Cleaning packages..."
sudo apt autoremove -y
