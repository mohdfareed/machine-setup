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
sh -c "$(curl -fsSL https://git.io/JvzfK)"
mkdir -p $HOME/.zsh

# auto completion
echo "Installing zsh-completions prompt..."
completions=$HOME/.zsh/zsh-completions; rm -rf $completions
git clone https://github.com/zsh-users/zsh-completions $completions

# pure prompt
echo "Installing pure prompt..."
pure=$HOME/.zsh/pure; rm -rf $pure
git clone https://github.com/sindresorhus/pure.git $pure

# clean packages
echo "Cleaning packages..."
sudo apt autoremove -y
