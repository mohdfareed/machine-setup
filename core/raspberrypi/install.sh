# update and upgrade
sudo apt update && sudo apt full-upgrade -y

# machine packages
sudo apt install git -y
sudo apt install zsh -y
sudo apt install bat -y
sudo apt install exa -y
sudo apt install micro -y
sudo apt install zsh-syntax-highlighting -y
sudo apt install zsh-autosuggestions -y
sudo apt install tailscale -y

# snap store and packages
sudo apt install snapd -y
sudo snap install core
sudo snap install btop

# adguard home
curl -s -S -L https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/master/scripts/install.sh | \
sh -s -- -v

# python version manager
curl https://pyenv.run | bash
# python build dependencies
# source: https://github.com/pyenv/pyenv/wiki#suggested-build-environment
sudo apt install build-essential libssl-dev zlib1g-dev libbz2-dev \
     libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils tk-dev \
     libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev-y llvm -y

# oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
      "" --unattended
# pure prompt
mkdir -p "$HOME/.zsh"
git clone https://github.com/sindresorhus/pure.git "$HOME/.zsh/pure"

# clean packages
sudo apt autoremove -y
