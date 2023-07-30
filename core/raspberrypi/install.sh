# update and upgrade
sudo apt update && sudo apt full-upgrade -y

# tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# machine packages
sudo apt install git zsh zsh-syntax-highlighting zsh-autosuggestions -y
sudo apt install bat exa micro code snapd -y
sudo snap install core btop docker

# pure prompt
mkdir -p "$HOME/.zsh"
git clone https://github.com/sindresorhus/pure.git "$HOME/.zsh/pure"
# oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
      "" --unattended

# clean packages
sudo apt autoremove -y
