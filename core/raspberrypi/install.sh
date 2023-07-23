# update and upgrade
sudo apt update && sudo apt full-upgrade -y

# machine packages
sudo apt install git zsh bat exa micro samba tailscale -y
sudo apt install zsh-syntax-highlighting zsh-autosuggestions -y
# snap store and packages
sudo apt install snapd -y
sudo snap install core btop

# adguard home
curl -s -S -L https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/master/scripts/install.sh | \
sh -s -- -v

# docker
curl -sSL https://get.docker.com | sh
# add user to docker group
sudo usermod -aG docker $USER

# python version manager
curl https://pyenv.run | bash
# python build dependencies
# source: https://github.com/pyenv/pyenv/wiki#suggested-build-environment
sudo apt install build-essential libssl-dev zlib1g-dev libbz2-dev \
     libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils tk-dev \
     libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev-y llvm -y

# pure prompt
mkdir -p "$HOME/.zsh"
git clone https://github.com/sindresorhus/pure.git "$HOME/.zsh/pure"
# oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
      "" --unattended

# clean packages
sudo apt autoremove -y
